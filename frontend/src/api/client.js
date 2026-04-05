import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 30_000,
})

// ── Metrics ──────────────────────────────────────────────────────────────────
export const fetchSummary = (params = {}) =>
  api.get('/metrics/summary', { params }).then(r => r.data)

export const fetchTimeseries = (params = {}) =>
  api.get('/metrics/timeseries', { params }).then(r => r.data)

export const fetchCategories = (params = {}) =>
  api.get('/metrics/categories', { params }).then(r => r.data)

export const fetchPayments = (params = {}) =>
  api.get('/metrics/payments', { params }).then(r => r.data)

// ── Anomaly ───────────────────────────────────────────────────────────────────
export const fetchAnomalies = (params = {}) =>
  api.get('/anomaly/detect', { params }).then(r => r.data)

// ── Forecast ──────────────────────────────────────────────────────────────────
export const fetchForecast = (params = {}) =>
  api.get('/forecast', { params }).then(r => r.data)

// ── Insights ──────────────────────────────────────────────────────────────────
export const fetchInsights = (params = {}) =>
  api.get('/insights', { params }).then(r => r.data)
