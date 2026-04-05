import React, { useState } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'

export default function App() {
  const [filters, setFilters]       = useState({})
  const [activeSection, setSection] = useState('overview')

  return (
    <div className="app-shell">
      <Sidebar
        filters={filters}
        onFiltersChange={setFilters}
        activeSection={activeSection}
        onSectionChange={setSection}
      />
      <main className="main-content">
        <Dashboard filters={filters} activeSection={activeSection} />
      </main>
    </div>
  )
}
