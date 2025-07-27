from fastapi import APIRouter, HTTPException, Query
from services.cnn_fetcher import one_year_prices, five_competitors
from services.tipranks_fetcher import forecast_price, smart_score
from services.auth import validate_credentials

router = APIRouter()

@router.get("/fetch")
async def fetch_all_data(
    id: str = Query(..., alias="id"),
    api_key: str = Query(..., alias="api-key"),
    ticker: str = Query(..., min_length=1, description="Ticker symbol, e.g., AAPL, TSLA")
):
    is_valid, message = validate_credentials(id, api_key)
    if not is_valid:
        raise HTTPException(status_code=403, detail=message)

    oneYearPrices = await one_year_prices(ticker)
    fiveCompetitors = await five_competitors(ticker)
    forecastPrices = await forecast_price(ticker)
    smartScoreData = await smart_score(ticker)

    return {
        "ticker": ticker.upper(),
        "one_year_prices": oneYearPrices,
        "five_competitors": fiveCompetitors,
        "forecast_price": forecastPrices,
        "smart_score": smartScoreData,
    }
