import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import create_app
from app.routes import blog, sections

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    pass

app = create_app()
app.router.lifespan_context = lifespan

# Include routers
app.include_router(sections.router)
app.include_router(blog.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
