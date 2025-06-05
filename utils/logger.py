from loguru import logger
from config import settings
import sys
import os

# Удаляем все обработчики
logger.remove()

# Получаем конфигурацию из .env
log_level = settings.log_level.upper()
log_file_path = settings.log_file
log_json = settings.log_json

# Убедимся, что директория существует
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Консольный логгер
if settings.log_json:
    logger.add(sys.stdout, level=log_level, serialize=True)
else:
    logger.add(sys.stdout, level=log_level, format="{time} | {level} | {message}")

# Файловый логгер
logger.add(
    log_file_path,
    level=log_level,
    serialize=log_json,
    rotation="10 MB",
    retention="7 days",
    compression="zip"
)
