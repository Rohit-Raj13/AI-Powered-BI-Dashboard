import React from 'react'

const CATEGORIES = ['All', 'Electronics', 'Clothing', 'Sports', 'Books', 'Toys', 'Beauty', 'Home & Kitchen']
const PAYMENTS   = ['All', 'Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery']

const NAV_ITEMS = [
  { id: 'overview',  label: 'Overview',          icon: '🏠' },
  { id: 'trends',    label: 'Trends & Analysis',  icon: '📊' },
  { id: 'anomalies', label: 'Anomaly Detection',  icon: '🚨' },
  { id: 'forecast',  label: 'Forecasting',        icon: '📈' },
  { id: 'insights',  label: 'AI Insights',        icon: '🧠' },
]

export default function Sidebar({ filters, onFiltersChange, activeSection, onSectionChange }) {
  const update = (key, val) => onFiltersChange({ ...filters, [key]: val || undefined })

  const reset = () => onFiltersChange({})

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h2>AI-Powered <span>BI Dashboard</span></h2>
        <p>E-Commerce Analytics Platform</p>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map(item => (
          <button key={item.id}
            className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
            onClick={() => onSectionChange(item.id)}>
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      <div className="filter-section">
        <div className="filter-label">Filters</div>

        <div className="filter-group">
          <label>Start Date</label>
          <input type="date" className="filter-input"
            value={filters.startDate || ''}
            min="2024-01-01" max="2024-11-30"
            onChange={e => update('startDate', e.target.value)} />
        </div>

        <div className="filter-group">
          <label>End Date</label>
          <input type="date" className="filter-input"
            value={filters.endDate || ''}
            min="2024-01-01" max="2024-11-30"
            onChange={e => update('endDate', e.target.value)} />
        </div>

        <div className="filter-group">
          <label>Category</label>
          <select className="filter-select"
            value={filters.category || ''}
            onChange={e => update('category', e.target.value)}>
            {CATEGORIES.map(c => (
              <option key={c} value={c === 'All' ? '' : c}>{c}</option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Payment Method</label>
          <select className="filter-select"
            value={filters.paymentMethod || ''}
            onChange={e => update('paymentMethod', e.target.value)}>
            {PAYMENTS.map(p => (
              <option key={p} value={p === 'All' ? '' : p}>{p}</option>
            ))}
          </select>
        </div>

        <button className="filter-reset-btn" onClick={reset}>↺ Reset Filters</button>
      </div>
    </aside>
  )
}
