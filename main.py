from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from config import settings  # ✅
from database.init_db import init_db
from middlewares.logging_middleware import LoggingMiddleware
from routers import monitoring_route
from routers import users_route, auth_route
from utils.logger import logger

# Разрешённые origins (тут React dev сервер — http://localhost:3000)
origins = [
    "http://localhost:3000",
    # Можно добавить сюда дополнительные origins, например:
    # "https://my-production-frontend.com",
]

logger.info("Приложение запущено")

init_db()

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(users_route.router)

app.include_router(auth_route.router)

app.include_router(monitoring_route.router)

# Подключение метрик
Instrumentator().instrument(app).expose(app)

# Подключаем middleware логирования
app.add_middleware(LoggingMiddleware)  # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешённые методы (GET, POST и т.п.)
    allow_headers=["*"],  # Разрешённые заголовки
)

for route in app.routes:
    print(route.path)
