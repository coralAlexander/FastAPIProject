import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
import json


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Читаем тело запроса (можно только один раз, поэтому сохраняем)
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8")
        try:
            body_data = json.loads(body_str) if body_str else {}
        except json.JSONDecodeError:
            body_data = body_str

        logger.info(f"Request: {request.method} {request.url.path} | From: {request.client.host} | Body: {body_data}")

        # Заменяем тело запроса на новое (иначе FastAPI не сможет прочитать его повторно)
        async def receive():
            return {"type": "http.request", "body": body_bytes}

        request._receive = receive

        # Получаем ответ
        response: Response = await call_next(request)

        # Читаем тело ответа (также читается только один раз)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        # Восстанавливаем response, чтобы FastAPI мог вернуть его клиенту
        response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )

        duration = time.time() - start_time
        try:
            response_data = json.loads(response_body.decode("utf-8"))
        except Exception:
            response_data = response_body.decode("utf-8", errors="ignore")

        logger.info(
            f"Response: {request.method} {request.url.path} - {response.status_code} - {duration:.2f}s | Body: {response_data}"
        )

        return response
