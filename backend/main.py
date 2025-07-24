import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.openapi.utils import get_openapi

from database import Base, engine
from routers import cases_router, clients_router # Add other routers as needed

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal Case Management System", version="1.0.0", openapi_url="/openapi.json", docs_url=None, redoc_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Replace with your allowed origins in production
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#Register routers
app.include_router(cases_router)
app.include_router(clients_router)


@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Legal Case Management System",
        version="1.0.0",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi


# Serve static files for frontend
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str, request: Request):
        if file_path.startswith("api"):
            return None  # Let API routes handle it
        static_file = os.path.join("static", file_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        return FileResponse("static/index.html")  # SPA routing


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
def all_exception_handler(request: Request, exc: Exception):
    # Log the exception
    import logging
    logging.exception(exc)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
