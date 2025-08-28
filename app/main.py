from fastapi import FastAPI

from .routes.auth import router as auth_router


app = FastAPI(
    title="TCGScan API",
    version="0.1.0",
    description=(
        "API for card recognition, collections, and deck management.\n\n"
        "Use the Authorize button to enter a Bearer token after logging in via /auth/login."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TCGScan"}
