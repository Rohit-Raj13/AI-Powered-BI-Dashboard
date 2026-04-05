import React, { useEffect, useRef, useState } from 'react'
import KPICard from '../components/KPICard'
import TimeSeriesChart from '../components/TimeSeriesChart'
import AnomalyChart from '../components/AnomalyChart'
import ForecastChart from '../components/ForecastChart'
import InsightsPanel from '../components/InsightsPanel'
import CategoryBreakdown from '../components/CategoryBreakdown'
import { useSummary } from '../api/hooks'

export default function Dashboard({ filters, activeSection }) {
  const { data: summary, isLoading: summaryLoading } = useSummary(filters)

  // Live WebSocket tick
  const [liveData, setLiveData] = useState(null)
  const wsRef = useRef(null)
  useEffect(() => {
    const connect = () => {
      try {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
        const ws = new WebSocket(`${protocol}://${window.location.host}/ws/live`)
        ws.onmessage = e => setLiveData(JSON.parse(e.data))
        ws.onerror   = () => ws.close()
        ws.onclose   = () => setTimeout(connect, 5000)
        wsRef.current = ws
      } catch (_) {}
    }
    connect()
    return () => wsRef.current?.close()
  }, [])

  const s = summary || {}

  return (
    <div>
      {/* ── Page Header ── */}
      <div className="page-header">
        <h1>
          Business Intelligence Dashboard
          <span className="live-badge">
            <span className="live-dot" />
            LIVE
          </span>
        </h1>
        <p>
          AI-powered analytics with anomaly detection, forecasting, and real-time insights
          {liveData && (
            <span style={{ marginLeft: 12, color: 'var(--accent-green)', fontSize: '0.78rem' }}>
              · Last snapshot: {liveData.ts?.slice(11, 19)} UTC
            </span>
          )}
        </p>
      </div>

      {/* ── KPI Cards ── */}
      <div className="kpi-grid">
        <KPICard label="Total Revenue"    icon="revenue"   value={summaryLoading ? '—' : s.total_revenue}    change={s.revenue_change_wow} changeLabel="WoW" />
        <KPICard label="Total Orders"     icon="orders"    value={summaryLoading ? '—' : s.total_orders}     noFormat change={null} />
        <KPICard label="Unique Customers" icon="customers" value={summaryLoading ? '—' : s.unique_customers} noFormat change={null} />
        <KPICard label="Avg Order Value"  icon="aov"       value={summaryLoading ? '—' : s.avg_order_value}  change={s.revenue_change_mom} changeLabel="MoM" />
        <KPICard label="Avg Discount"     icon="discount"  value={summaryLoading ? '—' : s.avg_discount_pct} suffix="%" noFormat change={null} />
        <KPICard label="Top Category"     icon="category"  value={summaryLoading ? '—' : s.top_category}     noFormat change={null} />
      </div>

      {/* ── Section: Overview / Trends ── */}
      {(activeSection === 'overview' || activeSection === 'trends') && (
        <>
          <div className="chart-grid" style={{ marginBottom: 20 }}>
            <TimeSeriesChart filters={filters} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <CategoryBreakdown filters={filters} />
            </div>
          </div>
        </>
      )}

      {/* ── Section: Anomalies ── */}
      {(activeSection === 'overview' || activeSection === 'anomalies') && (
        <div style={{ marginBottom: 20 }}>
          <AnomalyChart filters={filters} />
        </div>
      )}

      {/* ── Section: Forecast ── */}
      {(activeSection === 'overview' || activeSection === 'forecast') && (
        <div style={{ marginBottom: 20 }}>
          <ForecastChart filters={filters} />
        </div>
      )}

      {/* ── Section: Insights ── */}
      {(activeSection === 'overview' || activeSection === 'insights') && (
        <div className="bottom-grid">
          <InsightsPanel filters={filters} />
          <div className="card">
            <div className="card-title">Live Metrics Snapshot</div>
            {liveData ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                {[
                  { label: 'Latest Date',    value: liveData.latest_date },
                  { label: "Today's Revenue", value: `₹${Number(liveData.daily_revenue).toLocaleString('en-IN')}` },
                  { label: "Today's Orders",  value: liveData.daily_orders },
                  { label: 'Total Revenue',   value: `₹${Number(liveData.total_revenue).toLocaleString('en-IN')}` },
                  { label: 'Total Orders',    value: liveData.total_orders?.toLocaleString('en-IN') },
                ].map(({ label, value }) => (
                  <div key={label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                    padding: '10px 14px', background: 'var(--bg-glass)', borderRadius: 8,
                    border: '1px solid var(--border)' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{label}</span>
                    <span style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--accent-blue)' }}>{value}</span>
                  </div>
                ))}
                <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textAlign: 'center', marginTop: 4 }}>
                  Updates every 5 seconds via WebSocket
                </p>
              </div>
            ) : (
              <div className="loading-state">
                <div className="spinner" />
                <span>Connecting to live feed…</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
