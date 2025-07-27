import httpx

TIPRANKS_HEADERS = {
    "accept":  "application/json, text/plain, */*",
    "accept-encoding":  "gzip, deflate, br, zstd",
    "accept-language":  "en-US,en;q=0.9,id;q=0.8,fa;q=0.7,ar;q=0.6,ms;q=0.5,ja;q=0.4,es;q=0.3",
    "cookie":  "personal-message=none; tr-plan-id=0; tr-plan-name=free; tr-experiments-version=1.14; tipranks-experiments=%7b%22Experiments%22%3a%5b%7b%22Name%22%3a%22general_A%22%2c%22Variant%22%3a%22v2%22%2c%22SendAnalytics%22%3afalse%7d%2c%7b%22Name%22%3a%22general_B%22%2c%22Variant%22%3a%22v1%22%2c%22SendAnalytics%22%3afalse%7d%2c%7b%22Name%22%3a%22general_C%22%2c%22Variant%22%3a%22v7%22%2c%22SendAnalytics%22%3afalse%7d%5d%7d; tipranks-experiments-slim=general_A%3av2%7cgeneral_B%3av1%7cgeneral_C%3av7",
    "priority":  "u=1, i",
    "referer":  "https://www.tipranks.com/stocks/tsla/forecast",
    "sec-ch-ua":  '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    "sec-ch-ua-mobile":  "?0",
    "sec-ch-ua-platform":  "Windows",
    "sec-fetch-dest":  "empty",
    "sec-fetch-mode":  "cors",
    "sec-fetch-site":  "same-origin",
    "user-agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
}

async def forecast_price(ticker: str):
    url = f"https://www.tipranks.com/stocks/{ticker.lower()}/stock-forecast/payload.json"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=TIPRANKS_HEADERS)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        return {"error": f"Request error: {str(e)}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP status error: {e.response.status_code}"}

async def smart_score(ticker: str):
    url = f"https://widgets.tipranks.com/api/widgets/stockAnalysisOverview/?tickers={ticker.lower()}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=TIPRANKS_HEADERS)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        return {"error": f"Request error: {str(e)}"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP status error: {e.response.status_code}"}
