import React from 'react'
import { useInsights } from '../api/hooks'

const SEVERITY_CONFIG = {
  success: { bg: 'rgba(63,185,80,0.08)',  border: 'rgba(63,185,80,0.2)',  icon: '📈' },
  warning: { bg: 'rgba(240,136,62,0.08)', border: 'rgba(240,136,62,0.2)', icon: '⚠️' },
  danger:  { bg: 'rgba(248,81,73,0.08)',  border: 'rgba(248,81,73,0.2)',  icon: '🚨' },
  info:    { bg: 'rgba(88,166,255,0.08)', border: 'rgba(88,166,255,0.2)', icon: '💡' },
}

const TYPE_ICON = {
  trend: '📊', anomaly: '🚨', category: '🏆', payment: '💳', forecast: '📈',
}

export default function InsightsPanel({ filters }) {
  const { data, isLoading, isError } = useInsights(filters)
  const insights = data?.insights || []

  return (
    <div className="card" style={{ height: '100%' }}>
      <div className="card-title">
        AI Insights
        <span style={{
          background: 'rgba(188,140,255,0.15)', color: '#bc8cff',
          padding: '2px 10px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600,
        }}>
          {insights.length} insights
        </span>
      </div>

      {isLoading && <div className="loading-state"><div className="spinner" /><span>Generating insights…</span></div>}
      {isError   && <div className="error-state">⚠ Insights unavailable</div>}
      {!isLoading && !isError && (
        <div className="insights-list">
          {insights.map((ins, i) => {
            const cfg = SEVERITY_CONFIG[ins.severity] || SEVERITY_CONFIG.info
            return (
              <div key={ins.id}
                className={`insight-item sev-${ins.severity}`}
                style={{
                  background: cfg.bg,
                  borderColor: cfg.border,
                  animationDelay: `${i * 60}ms`,
                }}>
                <span className="insight-icon">{TYPE_ICON[ins.type] || '💡'}</span>
                <div className="insight-body">
                  <div className="insight-title">{ins.title}</div>
                  <div className="insight-desc">{ins.description}</div>
                </div>
                {ins.value && <span className="insight-value">{ins.value}</span>}
              </div>
            )
          })}
          {insights.length === 0 && (
            <div className="loading-state" style={{ padding: 24 }}>
              <span>No insights available for current filters</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
