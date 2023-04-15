# Bitpapa BOT

## Requirements
- Docker
- Docker Compose 

## Installation 

Create `.env` file. Fill it with values by example:
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bitpapa_bot
JWT_SECRET_KEY=secret_key
JWT_REFRESH_SECRET_KEY=refresh_secret_key
API_URL=http://localhost:8011/api/v1
```

Change `JWT_SECRET_KEY` and `JWT_REFRESH_SECRET_KEY` to whatever value you like. Change API_URL to your server URL.

Build docker containers:
```
docker compose build
```

Start docker containers:
```
docker compose up -d
```

Run migrations on database:
```
docker compose exec config_server alembic upgrade head
```

## Managing user

Create an user:
```
docker compose exec config_server ./xcli.py create_user <username> <password>
```

Change the user password:
```
docker compose exec config_server ./xcli.py change_password <username> <new_password>
```

Values:
- \<username> - username you would like to use.
- \<password> - password you would like to use.
- \<new_password> - password to change to.

## Security 

To reset all the accesses to the front go to `.env` and change values of `JWT_SECRET_KEY` and `JWT_REFRESH_SECRET_KEY`. Then run:
```
docker compose up -d --build
```

Every user after that should be logged out.

## Repository content
- Config server (FastAPI) - *./app/*.
- Config front (React) - *./config_front/*.
- Min price updater (HTTPX) - *./app/tasks/update_price_info.py*.
- Offer price updater (HTTPX) - *./app/tasks/update_offer.py*. 
- Dockerfiles - *./provision/*.
- docker-compose.yml for deployment - *./docker-compose.yml*.
- docker-compose.yml for local development - *./docker-compose.dev.yml*.


