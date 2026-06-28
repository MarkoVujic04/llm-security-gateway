from fastapi import FastAPI
from app.config import settings
from app.proxy.router import router as proxy_router

app = FastAPI(title=settings.app_name)
app.include_router(proxy_router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}
