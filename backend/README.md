# Backend Architecture

```
fastapi-backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── health.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging_config.py
│   ├── db/
│   │   └── mongodb.py
│   └── main.py
├── tests/
│   └── test_health.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .env.example
└── README.md
```
