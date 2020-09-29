# atptennisapi

API reference:

| Endpoint | Method |
| -------- | ------ |
| /api/v1/players | GET | 

API tests:

```bash
curl "https://atptennisapi.freeddns.org/api/v1/players"
curl "https://atptennisapi.freeddns.org/api/v1/tournaments"
curl "https://atptennisapi.freeddns.org/api/v1/matchups?tournament_name=Beijing&tournament_start_date=Mon%2C%2003%20Oct%202016%2000%3A00%3A00%20GMT"
```

Docker instructions:

```bash
docker build -t atptennisapi:latest .

# change SQLALCHEMY_DATABASE_URI, REDIS_HOST, REDIS_PORT as needed
docker run --name atptennisapi --restart always -e SQLALCHEMY_DATABASE_URI=<your_uri> -e REDIS_HOST=<your_host> -e REDIS_PASS=<your_pass> -p 5000:5000 -d atptennisapi:latest
```