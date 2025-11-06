# API Count Integration

Ce projet démontre comment appeler une API pour récupérer une valeur de count dans une application React avec Vite.

## Fonctionnalités implémentées

### Hook personnalisé `useCountApi`
- **Localisation :** `src/hooks/useCountApi.ts`
- **Fonction :** Gère les appels d'API avec gestion d'état complète
- **États gérés :**
  - `data`: La valeur du count récupérée
  - `loading`: État de chargement pour la récupération
  - `isIncrementing`: État de chargement pour l'incrémentation
  - `error`: Gestion des erreurs
- **Fonctions disponibles :**
  - `refetch`: Fonction pour relancer la récupération
  - `incrementCount`: Fonction pour incrémenter le count via API

### Composant App modifié
- **Localisation :** `src/App.tsx`
- **Affichage :**
  - Count depuis l'API avec états de chargement/erreur
  - **Bouton d'incrémentation** qui appelle l'endpoint d'incrémentation
  - Bouton pour actualiser les données
  - Count local pour comparaison
  - Gestion des erreurs utilisateur
  - États visuels pour les opérations en cours

### API utilisée
- **URL actuelle :** `https://jsonplaceholder.typicode.com/posts/1`
- **Format :** Récupère l'ID du post comme valeur de count
- **Personnalisation :** Facilement modifiable pour votre propre API

## Comment utiliser votre propre API

1. **Modifiez l'URL dans `App.tsx` :**
   ```typescript
   const API_URL = 'https://votre-api.com/count'
   ```

2. **Adaptez le format de réponse dans `useCountApi.ts` si nécessaire :**
   ```typescript
   interface CountResponse {
     count: number // Votre structure de données
   }
   ```

3. **Endpoints requis :**
   - `GET /count` - Récupérer la valeur actuelle
   - `POST /count/increment` - Incrémenter la valeur

4. **Format de réponse attendu :**
   ```json
   {
     "count": 42
   }
   ```

5. **Exemple d'implémentation serveur (Express.js) :**
   ```javascript
   // GET /api/count
   app.get('/api/count', (req, res) => {
     res.json({ count: currentCount })
   })
   
   // POST /api/count/increment
   app.post('/api/count/increment', (req, res) => {
     currentCount += 1
     res.json({ count: currentCount })
   })
   ```

## Gestion des erreurs
- Erreurs réseau automatiquement captées
- Codes d'état HTTP vérifiés
- Messages d'erreur affichés à l'utilisateur
- Possibilité de relancer la requête

## États de l'interface
- **Chargement :** Indicateur visuel pendant l'appel
- **Succès :** Affichage de la valeur récupérée
- **Erreur :** Message d'erreur clair avec possibilité de réessayer

## Démarrage
```bash
npm run dev
```

L'application sera disponible sur http://localhost:5173 (ou le prochain port libre).