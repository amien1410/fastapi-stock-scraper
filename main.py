from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Modular Stock Data Fetcher API",
    version="1.0",
    description="Fetch stock insights securely from CNN and TipRanks."
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "📈 Welcome to the Stock Data Fetcher API!",
        "about": (
            "This API securely fetches financial insights from CNN and TipRanks "
            "for authenticated users. Access the /fetch endpoint with valid ID and API key "
            "as query parameters (e.g., /fetch?id=your-id&api-key=your-key) to get real-time data."
        ),
        "endpoints": {
            "/fetch": "Returns JSON from CNN and TipRanks if authenticated",
        },
        "example": "/fetch?id=12345&api-key=abcdef"
    }
