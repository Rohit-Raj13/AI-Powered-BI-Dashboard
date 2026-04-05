import React from 'react'

const fmt = (v) => {
  if (typeof v !== 'number') return v
  if (v >= 1_000_000) return `₹${(v / 1_000_000).toFixed(1)}M`
  if (v >= 1_000)     return `₹${(v / 1_000).toFixed(1)}K`
  return `₹${v.toLocaleString('en-IN')}`
}

const ICONS = {
  revenue: '💰',
  orders: '🛒',
  customers: '👥',
  aov: '📊',
  discount: '🏷️',
  category: '🏆',
  payment: '💳',
}

export default function KPICard({ label, value, icon, change, changeLabel, prefix = '', suffix = '', noFormat = false }) {
  const isPositive = change > 0
  const isNeutral  = change === null || change === undefined

  return (
    <div className="kpi-card">
      <div className="kpi-header">
        <span className="kpi-label">{label}</span>
        <span className="kpi-icon">{ICONS[icon] || '📈'}</span>
      </div>
      <div className="kpi-value">
        {prefix}{noFormat ? value : fmt(value)}{suffix}
      </div>
      {!isNeutral && (
        <span className={`kpi-badge ${isPositive ? 'badge-up' : 'badge-down'}`}>
          {isPositive ? '↑' : '↓'} {Math.abs(change)}% {changeLabel || ''}
        </span>
      )}
      {isNeutral && value && typeof value === 'string' && (
        <span className="kpi-badge badge-neutral">{value}</span>
      )}
    </div>
  )
}
