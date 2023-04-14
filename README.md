# Bitpapa BOT

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

Create an user:
```
docker compose exec config_server ./xcli.py create_user <username> <password>
```

Values:
- \<username> - username you would like to use.
- \<password> - password you would like to use.
