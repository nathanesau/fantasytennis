# DNS entries

Table of entries:

| service | dns entry | dns provider | port (for nginx) | 
| ------- | --------- | -------------| ---------------- |
| atptennisapi | atptennisapi.freeddns.org | https://www.dynu.com | 5000 |
| cache | nathanesauredis.freeddns.org | https://www.dynu.com | 6379 |
| database | nathanesaupostgres.freeddns.org | https://www.dynu.com | 5432 |

# Environment variables

* POSTGRES_HOST
* POSTGRES_PASS
* REDIS_HOST
* REDIS_PASS

# certbot

use following command:

```bash
# C:\Certbot\live\atptennisapi.freeddns.org\fullchain.pem;
# C:\Certbot\live\atptennisapi.freeddns.org\privkey.pem;
certbot certonly -d atptennisapi.freeddns.org
```
