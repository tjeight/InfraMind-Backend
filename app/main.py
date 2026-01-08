from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.configs.session import engine
from app.repository.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify PostgreSQL connectivity
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ PostgreSQL connected successfully")
    except Exception as exc:
        print("❌ PostgreSQL connection failed")
        raise exc

    yield

    # Shutdown: release DB resources
    await engine.dispose()
    print("🛑 PostgreSQL engine disposed")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router)
