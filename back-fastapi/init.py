from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to FastAPI"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """Example endpoint with path and query parameters."""
    return {"item_id": item_id, "q": q}