# atptennisapi

API reference:

| Endpoint | Method |
| -------- | ------ |
| /api/v1/players | GET | 

API tests:

```bash
# {"players":[{"country_code":"SWI","id":1,"name":"Roger Federer"},{"country_code":"SPA","id":2,"name":"Rafael Nadal"}]}
curl -k https://localhost:5000/api/v1/players

# {"tournaments":[{"country_code":"SWI","id":1,"name":"Roger Federer"},{"country_code":"SPA","id":2,"name":"Rafael Nadal"}]}
curl -k https://localhost:5000/api/v1/tournaments

# 
```