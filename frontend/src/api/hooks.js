import { useQuery } from '@tanstack/react-query'
import {
  fetchAnomalies, fetchCategories, fetchForecast,
  fetchInsights, fetchPayments, fetchSummary, fetchTimeseries,
} from './client'

const makeParams = (filters) => {
  const p = {}
  if (filters?.startDate)     p.start_date = filters.startDate
  if (filters?.endDate)       p.end_date   = filters.endDate
  if (filters?.category)      p.category   = filters.category
  if (filters?.paymentMethod) p.payment_method = filters.paymentMethod
  return p
}

export const useSummary = (filters) =>
  useQuery({
    queryKey: ['summary', filters],
    queryFn:  () => fetchSummary(makeParams(filters)),
    refetchInterval: 30_000,
  })

export const useTimeseries = (filters, granularity = 'monthly') =>
  useQuery({
    queryKey: ['timeseries', filters, granularity],
    queryFn:  () => fetchTimeseries({ ...makeParams(filters), granularity }),
  })

export const useCategories = (filters) =>
  useQuery({
    queryKey: ['categories', filters],
    queryFn:  () => fetchCategories(makeParams(filters)),
  })

export const usePayments = (filters) =>
  useQuery({
    queryKey: ['payments', filters],
    queryFn:  () => fetchPayments(makeParams(filters)),
  })

export const useAnomalies = (filters) =>
  useQuery({
    queryKey: ['anomalies', filters],
    queryFn:  () => fetchAnomalies(makeParams(filters)),
    staleTime: 60_000,
  })

export const useForecast = (periods = 30, filters = {}) =>
  useQuery({
    queryKey: ['forecast', periods, filters],
    queryFn:  () => fetchForecast({ ...makeParams(filters), periods }),
    staleTime: 120_000,
  })

export const useInsights = (filters) =>
  useQuery({
    queryKey: ['insights', filters],
    queryFn:  () => fetchInsights(makeParams(filters)),
    refetchInterval: 60_000,
  })
