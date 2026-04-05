import React from 'react'
import { useCategories, usePayments } from '../api/hooks'

const CATEGORY_COLORS = [
  '#58a6ff', '#bc8cff', '#3fb950', '#f0883e', '#f85149', '#39d353', '#ffa657',
]

export default function CategoryBreakdown({ filters }) {
  const { data: catData, isLoading: catLoading } = useCategories(filters)
  const { data: pmData,  isLoading: pmLoading }  = usePayments(filters)

  const cats  = catData || []
  const maxRev = cats.length ? cats[0].revenue : 1

  const payments = pmData || []

  return (
    <>
      {/* Category Breakdown */}
      <div className="card">
        <div className="card-title">Revenue by Category</div>
        {catLoading
          ? <div className="loading-state"><div className="spinner" /></div>
          : (
            <div className="category-list">
              {cats.map((c, i) => (
                <div key={c.category} className="category-item">
                  <div className="category-header">
                    <span className="category-name">{c.category}</span>
                    <span className="category-value">
                      ₹{(c.revenue / 1000).toFixed(1)}K
                      <span style={{ color: 'var(--text-muted)', marginLeft: 6 }}>
                        {c.share_pct}%
                      </span>
                    </span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill"
                      style={{
                        width: `${(c.revenue / maxRev) * 100}%`,
                        background: CATEGORY_COLORS[i % CATEGORY_COLORS.length],
                      }} />
                  </div>
                </div>
              ))}
            </div>
          )
        }
      </div>

      {/* Payment Methods */}
      <div className="card">
        <div className="card-title">Payment Methods</div>
        {pmLoading
          ? <div className="loading-state"><div className="spinner" /></div>
          : (
            <div className="category-list">
              {payments.map((p, i) => (
                <div key={p.payment_method} className="category-item">
                  <div className="category-header">
                    <span className="category-name">{p.payment_method}</span>
                    <span className="category-value">
                      {p.orders.toLocaleString('en-IN')} orders
                      <span style={{ color: 'var(--text-muted)', marginLeft: 6 }}>
                        {p.share_pct}%
                      </span>
                    </span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill"
                      style={{
                        width: `${p.share_pct}%`,
                        background: CATEGORY_COLORS[(i + 2) % CATEGORY_COLORS.length],
                      }} />
                  </div>
                </div>
              ))}
            </div>
          )
        }
      </div>
    </>
  )
}
