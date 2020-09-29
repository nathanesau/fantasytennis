# atptennisapi

API reference:

| Endpoint | Method |
| -------- | ------ |
| /api/v1/players | GET | 

API tests:

```bash
# {"players":[{"country_code":"SWI","id":1,"name":"Roger Federer"},{"country_code":"SPA","id":2,"name":"Rafael Nadal"}]}
curl https://atptennisapi.freeddns.org/api/v1/players
curl http://localhost:5000/api/v1/players

# {"tournaments":[{"country_code":"SWI","id":1,"name":"Roger Federer"},{"country_code":"SPA","id":2,"name":"Rafael Nadal"}]}
curl https://atptennisapi.freeddns.org/api/v1/tournaments
curl https://localhost:5000/api/v1/tournaments
```

Docker instructions:

```bash
docker build -t atptennisapi:latest .

# change SQLALCHEMY_DATABASE_URI, REDIS_HOST, REDIS_PORT as needed
docker run --name atptennisapi --restart always -e SQLALCHEMY_DATABASE_URI=<your_uri> -e REDIS_HOST=<your_host> -e REDIS_PASS=<your_pass> -p 5000:5000 -d atptennisapi:latest
```