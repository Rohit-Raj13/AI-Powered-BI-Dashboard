import React, { useState } from 'react'
import {
  ComposedChart, Area, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'
import { useForecast } from '../api/hooks'

const ForecastTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  const d = payload[0]?.payload || {}
  return (
    <div className="custom-tooltip">
      <p style={{ fontWeight: 600, color: '#e6edf3', marginBottom: 4 }}>{label}</p>
      <p>Forecast: <b>₹{Number(d.yhat || 0).toLocaleString('en-IN')}</b></p>
      <p style={{ color: '#8b949e', fontSize: '0.72rem' }}>
        95% CI: ₹{Number(d.yhat_lower || 0).toLocaleString('en-IN')} – ₹{Number(d.yhat_upper || 0).toLocaleString('en-IN')}
      </p>
      {d.is_forecast && <p style={{ color: '#bc8cff', fontSize: '0.72rem', marginTop: 4 }}>📈 Projected</p>}
    </div>
  )
}

export default function ForecastChart({ filters }) {
  const [periods, setPeriods] = useState(30)
  const { data, isLoading, isError } = useForecast(periods, filters)

  // Merge history (last 60 pts) + forecast for one continuous chart
  const histSlice = (data?.history || []).slice(-60)
  const foreSlice = data?.forecast || []
  const rows = [...histSlice, ...foreSlice]

  const splitIdx = histSlice.length > 0 ? histSlice[histSlice.length - 1]?.ds : null

  return (
    <div className="card chart-full">
      <div className="card-title">
        Revenue Forecast
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Periods:</span>
          {[15, 30, 60, 90].map(p => (
            <button key={p} className={`tab-btn ${periods === p ? 'active' : ''}`}
              style={{ padding: '3px 9px', fontSize: '0.7rem' }}
              onClick={() => setPeriods(p)}>{p}d</button>
          ))}
        </div>
      </div>

      {isLoading && <div className="loading-state"><div className="spinner" /><span>Running forecast model…</span></div>}
      {isError   && <div className="error-state">⚠ Forecast failed</div>}
      {!isLoading && !isError && (
        <>
          <ResponsiveContainer width="100%" height={260}>
            <ComposedChart data={rows} margin={{ top: 4, right: 8, bottom: 4, left: 0 }}>
              <defs>
                <linearGradient id="ciGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#bc8cff" stopOpacity={0.25} />
                  <stop offset="100%" stopColor="#bc8cff" stopOpacity={0.03} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="ds" tick={{ fill: '#8b949e', fontSize: 10 }} tickLine={false} axisLine={false}
                interval={Math.max(1, Math.floor(rows.length / 12))}
                tickFormatter={v => v?.slice(5)} />
              <YAxis tick={{ fill: '#8b949e', fontSize: 11 }} tickLine={false} axisLine={false} width={52}
                tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v} />
              <Tooltip content={<ForecastTooltip />} />
              {splitIdx && (
                <ReferenceLine x={splitIdx} stroke="rgba(255,255,255,0.15)" strokeDasharray="6 3"
                  label={{ value: 'Today', fill: '#8b949e', fontSize: 10, position: 'top' }} />
              )}
              {/* CI band */}
              <Area type="monotone" dataKey="yhat_upper" stroke="none" fill="url(#ciGrad)" legendType="none" />
              <Area type="monotone" dataKey="yhat_lower" stroke="none" fill="var(--bg-primary)" legendType="none" />
              {/* Historical */}
              <Line type="monotone" dataKey="yhat"
                stroke="#58a6ff" strokeWidth={2} dot={false} activeDot={{ r: 4 }}
                strokeDasharray={undefined}
                connectNulls
              />
            </ComposedChart>
          </ResponsiveContainer>
          <div className="anomaly-legend">
            <div className="anomaly-legend-item">
              <div className="legend-dot" style={{ background: '#58a6ff' }} />
              <span>Historical / Fitted</span>
            </div>
            <div className="anomaly-legend-item">
              <div className="legend-dot" style={{ background: '#bc8cff' }} />
              <span>Forecast (next {periods} days)</span>
            </div>
            <div className="anomaly-legend-item">
              <div style={{ width: 16, height: 10, background: 'rgba(188,140,255,0.2)', borderRadius: 2 }} />
              <span>95% Confidence Interval</span>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
