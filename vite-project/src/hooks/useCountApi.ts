import { useState, useEffect, useCallback } from 'react'

interface CountResponse {
  count?: number
  id?: number // Pour JSONPlaceholder
}

interface ApiState {
  data: number | null
  loading: boolean
  error: string | null
  incrementLoading?: boolean
}

const useCountApi = (apiUrl: string) => {
  const [state, setState] = useState<ApiState>({
    data: null,
    loading: true,
    error: null,
    incrementLoading: false
  })

  const fetchCount = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }))
    
    try {
      const response = await fetch(apiUrl)
      
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
      
      const data: CountResponse = await response.json()
      
      // Gère différents formats d'API (count ou id)
      const countValue = data.count ?? data.id ?? 0
      
      setState({
        data: countValue,
        loading: false,
        error: null
      })
    } catch (error) {
      setState({
        data: null,
        loading: false,
        error: error instanceof Error ? error.message : 'Erreur inconnue'
      })
    }
  }, [apiUrl])

  useEffect(() => {
    fetchCount()
  }, [fetchCount])

  const incrementCount = useCallback(async () => {
    setState(prev => ({ ...prev, incrementLoading: true, error: null }))
    
    try {
      // Pour cet exemple, j'utilise un endpoint d'incrémentation simulé
      // Remplacez cette URL par votre véritable endpoint d'incrémentation
      // ensure we append /increment to the base API url without duplicating slashes
      const base = apiUrl.replace(/\/$/, '')
      const incrementUrl = `${base}/increment`
      
      const response = await fetch(incrementUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'increment' })
      })
      
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`)
      }
      
      const data: CountResponse = await response.json()
      const countValue = data.count ?? data.id ?? (state.data ?? 0) + 1
      
      setState(prev => ({
        ...prev,
        data: countValue,
        incrementLoading: false,
        error: null
      }))
    } catch (err) {
      // Do not silently increment locally on failure — surface the error so the
      // user can retry and the UI stays consistent with the server state.
      console.error('Erreur lors de l\'incrémentation:', err)
      setState(prev => ({
        ...prev,
        incrementLoading: false,
        error: err instanceof Error ? err.message : 'Erreur inconnue'
      }))
      throw err
    }
  }, [apiUrl, state.data])

  const refetch = () => {
    fetchCount()
  }

  return { 
    ...state, 
    refetch, 
    incrementCount,
    isIncrementing: state.incrementLoading 
  }
}

export default useCountApi