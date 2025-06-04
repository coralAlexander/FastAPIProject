from fastapi import FastAPI
from api.routes import router
from config import settings  # ✅
from database.session import engine
from database.init_db import init_db
from routers import users



app = FastAPI(title=settings.app_name)
app.include_router(users.router)

app.include_router(router)

@app.post("/test")
def test_post():
    return {"status": "OK"}

@app.get("/")
def read_root():
    return {
        "message": "FastAPI работает!",
        "debug": settings.debug
    }
init_db()


for route in app.routes:
    print(route.path)
