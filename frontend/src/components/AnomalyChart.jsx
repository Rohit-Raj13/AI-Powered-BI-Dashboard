import React from 'react'
import {
  ComposedChart, Line, Scatter, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'
import { useAnomalies } from '../api/hooks'

const SEVERITY_COLOR = { high: '#f85149', medium: '#f0883e', low: '#58a6ff' }

const CustomDot = (props) => {
  const { cx, cy, payload } = props
  if (!payload.is_anomaly) return null
  const color = SEVERITY_COLOR[payload.severity] || '#f85149'
  return (
    <g>
      <circle cx={cx} cy={cy} r={7} fill={color} fillOpacity={0.2} stroke={color} strokeWidth={2} />
      <circle cx={cx} cy={cy} r={3} fill={color} />
    </g>
  )
}

const AnomalyTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const d = payload[0]?.payload
  return (
    <div className="custom-tooltip">
      <p style={{ fontWeight: 600, color: '#e6edf3', marginBottom: 4 }}>{d?.date}</p>
      <p>Revenue: <b>₹{Number(d?.revenue).toLocaleString('en-IN')}</b></p>
      <p>Orders: <b>{d?.orders}</b></p>
      {d?.is_anomaly && (
        <>
          <p style={{ color: SEVERITY_COLOR[d.severity], marginTop: 6, fontWeight: 600 }}>
            ⚠ Anomaly ({d.severity.toUpperCase()})
          </p>
          <p style={{ fontSize: '0.72rem', color: '#8b949e', maxWidth: 260, marginTop: 4, lineHeight: 1.5 }}>
            {d.explanation}
          </p>
        </>
      )}
    </div>
  )
}

export default function AnomalyChart({ filters }) {
  const { data, isLoading, isError } = useAnomalies(filters)

  const rows     = data?.all_dates || []
  const nAnomaly = data?.total_anomalies || 0
  const mean     = rows.length ? rows.reduce((s,r) => s + r.revenue, 0) / rows.length : 0

  return (
    <div className="card chart-full">
      <div className="card-title">
        Anomaly Detection
        <span style={{
          background: nAnomaly > 0 ? 'rgba(248,81,73,0.15)' : 'rgba(63,185,80,0.15)',
          color: nAnomaly > 0 ? '#f85149' : '#3fb950',
          padding: '2px 10px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 700,
        }}>
          {nAnomaly} anomal{nAnomaly === 1 ? 'y' : 'ies'} detected
        </span>
      </div>

      {isLoading && <div className="loading-state"><div className="spinner" /><span>Running anomaly detection…</span></div>}
      {isError   && <div className="error-state">⚠ Anomaly detection failed</div>}
      {!isLoading && !isError && (
        <>
          <ResponsiveContainer width="100%" height={240}>
            <ComposedChart data={rows} margin={{ top: 4, right: 8, bottom: 4, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="date" tick={{ fill: '#8b949e', fontSize: 10 }} tickLine={false} axisLine={false}
                interval={Math.max(1, Math.floor(rows.length / 10))}
                tickFormatter={v => v?.slice(5)} />
              <YAxis tick={{ fill: '#8b949e', fontSize: 11 }} tickLine={false} axisLine={false} width={52}
                tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v} />
              <Tooltip content={<AnomalyTooltip />} />
              <ReferenceLine y={mean} stroke="rgba(255,255,255,0.12)" strokeDasharray="6 3"
                label={{ value: 'Avg', fill: '#484f58', fontSize: 10, position: 'right' }} />
              <Line type="monotone" dataKey="revenue" stroke="#58a6ff" strokeWidth={1.5}
                dot={<CustomDot />} activeDot={{ r: 5, strokeWidth: 0 }} />
            </ComposedChart>
          </ResponsiveContainer>
          <div className="anomaly-legend">
            <div className="anomaly-legend-item">
              <div className="legend-dot" style={{ background: '#f85149' }} />
              <span>High severity</span>
            </div>
            <div className="anomaly-legend-item">
              <div className="legend-dot" style={{ background: '#f0883e' }} />
              <span>Medium severity</span>
            </div>
            <div className="anomaly-legend-item">
              <div className="legend-dot" style={{ background: '#58a6ff' }} />
              <span>Low severity</span>
            </div>
            <div className="anomaly-legend-item" style={{ marginLeft: 'auto' }}>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>
                Methods: Z-score (±2.5σ) + Isolation Forest
              </span>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
