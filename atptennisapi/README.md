# atptennisapi

API tests:

```bash
curl "https://atptennisapi.freeddns.org/players"
curl "https://atptennisapi.freeddns.org/player?id=1"
curl "https://atptennisapi.freeddns.org/tournaments"
curl "https://atptennisapi.freeddns.org/tournament?id=1"
curl "https://atptennisapi.freeddns.org/matchups?tournament_name=Beijing&tournament_start_date=Mon%2C%2003%20Oct%202016%2000%3A00%3A00%20GMT"
```

Docker instructions:

```bash
docker build -t atptennisapi:latest .

# change SQLALCHEMY_DATABASE_URI, REDIS_HOST, REDIS_PORT as needed
docker run --name atptennisapi --restart always -e SQLALCHEMY_DATABASE_URI=<your_uri> -e REDIS_HOST=<your_host> -e REDIS_PASS=<your_pass> -p 5000:5000 -d atptennisapi:latest
```