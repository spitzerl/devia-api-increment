# Démarche pour lancer le projet avec docker-compose

## Prérequis
- Docker et docker-compose (ou Docker Compose v2) installés sur la machine.
- Être placé à la racine du dépôt où se trouve `docker-compose.yml`.

## Préparation
1. Copier/ajuster les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env pour renseigner URL, ports, mots de passe et credentials nécessaires
```

## Validation du fichier
```bash
docker-compose config
```

## Construction et démarrage
- Pour (re)construire les images et démarrer les services en arrière-plan :
```bash
docker-compose up -d --build
```
- Avec Docker Compose v2 :
```bash
docker compose up -d --build
```

## Vérification
- Lister les conteneurs en cours d'exécution :
```bash
docker-compose ps
```
- Suivre les logs (globaux ou d'un service) :
```bash
docker-compose logs -f
docker-compose logs -f <nom_du_service>
```

## Commandes fréquentes
- Voir les logs d'un service :
```bash
docker-compose logs -f <service>
```
- Ouvrir un shell dans un conteneur :
```bash
docker-compose exec <service> sh
# ou
docker-compose exec <service> bash
```
- Exécuter une commande ponctuelle (ex. migrations) :
```bash
docker-compose run --rm <service> <commande>
# Exemple : docker-compose run --rm app python manage.py migrate
```

## Arrêt et nettoyage
- Arrêter les services :
```bash
docker-compose stop
```
- Arrêter et supprimer les conteneurs (et réseaux associés) :
```bash
docker-compose down
```
- Supprimer aussi les volumes (perte des données persistées) :
```bash
docker-compose down -v
```

## Mises à jour et rebuild
```bash
docker-compose pull
docker-compose up -d --build
```

## Conseils pratiques
- `depends_on` ne garantit pas que la base de données est prête : utiliser un script wait-for / healthcheck ou relancer la migration avec des retries.
- Pour debugger, lancer sans `-d` pour voir tout en direct :
```bash
docker-compose up --build
```
- Ajouter un `docker-compose.override.yml` local pour surcharger des paramètres en dev (ports, volumes, etc.) sans modifier le fichier principal.

## En cas d'erreur
- Consulter les logs du service concerné :
```bash
docker-compose logs <service>
```
- Vérifier les variables d'environnement dans `.env` (URL DB, credentials, etc.).

## Remarque
- Adapter les noms de services (`<service>`, `app`, `db`, etc.) aux valeurs définies dans votre `docker-compose.yml`.