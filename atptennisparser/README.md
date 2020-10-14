# atptennisparser

Docker instructions:

```bash
docker build -t atptennisparser:latest .

# change SQLALCHEMY_DATABASE_URI as needed
docker run --name atptennisparser --restart always -e SQLALCHEMY_DATABASE_URI=<your_uri> -d -v D:/atptourdata:/root/data -v D:/logs:/root/logs atptennisparser:latest
```