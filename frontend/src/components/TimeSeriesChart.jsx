import React, { useState } from 'react'
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Brush, Legend,
} from 'recharts'
import { useTimeseries } from '../api/hooks'

const COLORS = { revenue: '#58a6ff', orders: '#bc8cff' }

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <p style={{ fontWeight: 600, marginBottom: 6, color: '#e6edf3' }}>{label}</p>
      {payload.map(p => (
        <p key={p.name} style={{ color: p.color }}>
          {p.name === 'revenue' ? `₹${Number(p.value).toLocaleString('en-IN')}` : `${p.value} orders`}
        </p>
      ))}
    </div>
  )
}

export default function TimeSeriesChart({ filters }) {
  const [granularity, setGranularity] = useState('monthly')
  const [metric, setMetric] = useState('revenue')
  const { data, isLoading, isError } = useTimeseries(filters, granularity)

  const rows = data?.data || []

  return (
    <div className="card">
      <div className="card-title">
        Revenue & Orders Trend
        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
          {rows.length} data points
        </span>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 14, flexWrap: 'wrap' }}>
        <div className="chart-toolbar">
          {['daily', 'weekly', 'monthly'].map(g => (
            <button key={g} className={`tab-btn ${granularity === g ? 'active' : ''}`}
              onClick={() => setGranularity(g)}>{g.charAt(0).toUpperCase() + g.slice(1)}</button>
          ))}
        </div>
        <div className="chart-toolbar">
          {['revenue', 'orders', 'both'].map(m => (
            <button key={m} className={`tab-btn ${metric === m ? 'active' : ''}`}
              onClick={() => setMetric(m)}>{m.charAt(0).toUpperCase() + m.slice(1)}</button>
          ))}
        </div>
      </div>

      {isLoading && <div className="loading-state"><div className="spinner" /><span>Loading chart…</span></div>}
      {isError  && <div className="error-state">⚠ Failed to load timeseries data</div>}
      {!isLoading && !isError && (
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={rows} margin={{ top: 4, right: 8, bottom: 4, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
            <XAxis dataKey="period" tick={{ fill: '#8b949e', fontSize: 11 }}
              tickLine={false} axisLine={false}
              tickFormatter={v => {
                if (granularity === 'daily') return v.slice(5)   // MM-DD
                if (granularity === 'weekly') return v.slice(0, 10)
                return v  // monthly YYYY-MM
              }} />
            <YAxis tick={{ fill: '#8b949e', fontSize: 11 }} tickLine={false} axisLine={false}
              tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v}
              width={48} />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(88,166,255,0.2)', strokeWidth: 2 }} />
            {(metric === 'revenue' || metric === 'both') && (
              <Line type="monotone" dataKey="revenue" stroke={COLORS.revenue} strokeWidth={2}
                dot={false} activeDot={{ r: 5, strokeWidth: 0 }} name="revenue" />
            )}
            {(metric === 'orders' || metric === 'both') && (
              <Line type="monotone" dataKey="orders" stroke={COLORS.orders} strokeWidth={2}
                dot={false} activeDot={{ r: 5, strokeWidth: 0 }} name="orders"
                yAxisId={metric === 'both' ? 'right' : undefined} />
            )}
            {rows.length > 20 && <Brush dataKey="period" height={22} stroke="rgba(255,255,255,0.06)"
              fill="rgba(22,27,34,0.9)" travellerWidth={6} />}
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
