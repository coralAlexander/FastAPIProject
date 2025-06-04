from pydantic_settings import BaseSettings  # ✅
# или, если используешь Pydantic <2.0:
# from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = True

    db_user: str
    db_pass: str
    db_host: str
    db_name: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"

# ⬇️ вот это обязательно должно быть
settings = Settings()
