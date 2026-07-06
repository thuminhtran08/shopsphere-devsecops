from fastapi import FastAPI

app = FastAPI(
    title="ShopSphere Auth Service",
    description="Authentication service for ShopSphere DevSecOps Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "service": "auth-service",
        "message": "ShopSphere Auth Service is running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "auth-service",
    }