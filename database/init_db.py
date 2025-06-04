from database.session import engine
from models.base import Base
from models import user  # ⬅️ Импорт нужен, чтобы SQLAlchemy знал о модели

def init_db():
    Base.metadata.create_all(bind=engine)
