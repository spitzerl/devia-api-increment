import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import useCountApi from './hooks/useCountApi'

function App() {
  const [localCount, setLocalCount] = useState(0)
  
  // API URL: configurable via Vite env VITE_API_URL, sinon utilise le backend local
  // Exemple pour dev: VITE_API_URL="http://localhost:8000/api/count"
  const API_URL = import.meta.env.VITE_API_URL || '/api/count'
  const { 
    data: apiCount, 
    loading, 
    error, 
    refetch, 
    incrementCount, 
    isIncrementing 
  } = useCountApi(API_URL)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <div style={{ marginBottom: '1rem' }}>
          <h3>Count depuis l'API</h3>
          {loading && <p>Chargement...</p>}
          {error && <p style={{ color: 'red' }}>Erreur: {error}</p>}
          {apiCount !== null && (
            <p>Count depuis l'API: <strong>{apiCount}</strong></p>
          )}
          
          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button 
              onClick={incrementCount} 
              disabled={loading || isIncrementing}
              style={{ 
                backgroundColor: isIncrementing ? '#ccc' : '#646cff',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '8px',
                cursor: loading || isIncrementing ? 'not-allowed' : 'pointer'
              }}
            >
              {isIncrementing ? 'Incrémentation...' : 'Incrémenter Count'}
            </button>
            
            <button 
              onClick={refetch} 
              disabled={loading || isIncrementing}
              style={{ 
                backgroundColor: '#f9f9f9',
                border: '1px solid #ccc',
                padding: '10px 20px',
                borderRadius: '8px',
                cursor: loading || isIncrementing ? 'not-allowed' : 'pointer'
              }}
            >
              Actualiser
            </button>
          </div>
        </div>
        
        <div>
          <h3>Count local (pour comparaison)</h3>
          <button onClick={() => setLocalCount((prev) => prev + 1)}>
            Count local est {localCount}
          </button>
        </div>
        
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
