// Service pour simuler l'API d'incrémentation
// Dans un vrai projet, remplacez ceci par vos vrais endpoints API

export interface IncrementApiResponse {
  count: number
  message?: string
}

export const createIncrementApi = () => {
  let currentCount = 1

  const incrementCount = async (): Promise<IncrementApiResponse> => {
    // Simule un délai réseau
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Simule occasionnellement une erreur (5% de chance)
    if (Math.random() < 0.05) {
      throw new Error('Erreur serveur lors de l\'incrémentation')
    }
    
    currentCount += 1
    
    return {
      count: currentCount,
      message: 'Count incrémenté avec succès'
    }
  }

  const getCount = async (): Promise<IncrementApiResponse> => {
    await new Promise(resolve => setTimeout(resolve, 300))
    
    return {
      count: currentCount,
      message: 'Count récupéré avec succès'
    }
  }

  return {
    incrementCount,
    getCount,
    getCurrentCount: () => currentCount
  }
}

// Exemple d'utilisation avec une vraie API REST
export const realApiExample = {
  // GET /api/count - Récupérer le count actuel
  getCount: async (baseUrl: string) => {
    const response = await fetch(`${baseUrl}/api/count`)
    return response.json()
  },
  
  // POST /api/count/increment - Incrémenter le count
  incrementCount: async (baseUrl: string) => {
    const response = await fetch(`${baseUrl}/api/count/increment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ action: 'increment' })
    })
    return response.json()
  }
}