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
```

Change `JWT_SECRET_KEY` and `JWT_REFRESH_SECRET_KEY` to whatever value you like.

Build docker containers:
```
docker compose build --build-arg API_URL=<your url>
```
<your url> - URL of your server, or `http://localhost:8011` for local use.

Start docker containers:
```
docker compose up -d
```

Run migrations on database:
```
docker compose exec bitpapa_bot alembic upgrade head
```

Create an user:
```
docker compose exec bitpapa_bot ./xcli.py create_user <username> <password>
```

Values:
- \<username> - username you would like to use.
- \<password> - password you would like to use.
