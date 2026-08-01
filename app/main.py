import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base
from app.routers import predict, history, analytics
from app.services.ml_service import ensure_model_loaded
from app.utils import logger

# Lifespan event handler for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing SQLite database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Verifying ML Model artifacts...")
    ensure_model_loaded()
    yield
    # Shutdown actions
    logger.info("Shutting down Diabetes ML Application.")

app = FastAPI(
    title="GlucoPredict — Diabetes Risk Machine Learning Application",
    description="Full-stack machine learning web application using Scikit-Learn, FastAPI, Plotly, SQLite, and Bootstrap 5.",
    version="1.0.0",
    lifespan=lifespan
)

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include Routers
app.include_router(predict.router)
app.include_router(history.router)
app.include_router(analytics.router)

# Page Rendering Routes
@app.get("/", response_class=HTMLResponse)
def render_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict", response_class=HTMLResponse)
def render_predict_page(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def render_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/eda", response_class=HTMLResponse)
def render_eda_page(request: Request):
    return templates.TemplateResponse("eda.html", {"request": request})

@app.get("/models", response_class=HTMLResponse)
def render_models_page(request: Request):
    return templates.TemplateResponse("models.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
def render_history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

# Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation Error at {request.url.path}: {exc}")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error": "Invalid clinical input parameters provided."},
        status_code=422
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
