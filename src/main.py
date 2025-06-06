import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
import uvicorn


from src.api.auth import router as router_auth
from src.init import redis_manager

sys.path.append(str(Path(__file__).parent.parent))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключаемся к Redis при старте приложения
    await redis_manager.connect()
    yield
    # Закрываем подключение при завершении
    await redis_manager.close()

app = FastAPI(title="Task manager Docs", lifespan=lifespan)


app.include_router(router_auth)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)


