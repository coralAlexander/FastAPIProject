from fastapi import FastAPI
from config import settings  # ✅
from database.session import engine
from database.init_db import init_db
from routers import users
from utils.logger import logger
from prometheus_fastapi_instrumentator import Instrumentator
from routers import monitoring
from middlewares.logging_middleware import LoggingMiddleware


logger.info("Приложение запущено")

init_db()

app = FastAPI(title=settings.app_name , debug=settings.debug)
app.include_router(users.router)

app.include_router(monitoring.router)

# Подключение метрик
Instrumentator().instrument(app).expose(app)

# Подключаем middleware логирования
app.add_middleware(LoggingMiddleware) # type: ignore

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
