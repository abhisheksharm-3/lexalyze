from fastapi import FastAPI
from .routes import router
from . import create_app

app = create_app()
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)