# Database

running postgres docker for database:

```bash
docker run -p 5432:5432 --name postgres --restart always -e POSTGRES_PASSWORD=<pass> -d postgres
```
