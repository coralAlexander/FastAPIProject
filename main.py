import app
from fastapi import FastAPI
from config import settings  # ✅
from database.session import engine
from database.init_db import init_db
from routers import users, auth
from utils.logger import logger
from prometheus_fastapi_instrumentator import Instrumentator
from routers import monitoring
from middlewares.logging_middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware


# Разрешённые origins (тут React dev сервер — http://localhost:3000)
origins = [
    "http://localhost:3000",
    # Можно добавить сюда дополнительные origins, например:
    # "https://my-production-frontend.com",
]

logger.info("Приложение запущено")

init_db()

app = FastAPI(title=settings.app_name , debug=settings.debug)
app.include_router(users.router)

app.include_router(auth.router)

app.include_router(monitoring.router)

# Подключение метрик
Instrumentator().instrument(app).expose(app)

# Подключаем middleware логирования
app.add_middleware(LoggingMiddleware) # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],              # Разрешённые методы (GET, POST и т.п.)
    allow_headers=["*"],              # Разрешённые заголовки
)

@app.post("/test")
def test_post():
    return {"status": "OK"}

@app.get("/")
def read_root():
    return {
        "message": "FastAPI работает!",
        "debug": settings.debug
    }

for route in app.routes:
    print(route.path)
