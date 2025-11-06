// Simulateur d'API pour les tests locaux
// Vous pouvez l'utiliser en remplaçant l'URL dans App.tsx

export const mockApiServer = () => {
  // Simule un délai réseau
  const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))
  
  // Simule une réponse d'API avec un count aléatoire
  const getMockCount = async (): Promise<{ count: number }> => {
    await delay(1000) // Simule 1 seconde de latence
    
    // 90% de chance de succès, 10% d'erreur pour tester la gestion d'erreur
    if (Math.random() < 0.1) {
      throw new Error('Erreur simulée du serveur')
    }
    
    return {
      count: Math.floor(Math.random() * 100)
    }
  }
  
  return { getMockCount }
}

// Pour utiliser une vraie API, remplacez l'URL dans App.tsx par quelque chose comme :
// const API_URL = 'https://jsonplaceholder.typicode.com/posts/1'
// Mais n'oubliez pas d'adapter la structure de réponse dans le hook useCountApi