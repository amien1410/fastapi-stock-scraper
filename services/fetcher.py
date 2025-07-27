import httpx

URLS = [
    "https://production.dataviz.cnn.io/charting/instruments/cmg/1Y/false",
    "https://widgets.tipranks.com/api/widgets/stockAnalysisOverview/?tickers=vnet"
]

async def fetch_data_sources():
    async with httpx.AsyncClient(timeout=10) as client:
        results = {}
        for i, url in enumerate(URLS):
            try:
                response = await client.get(url)
                response.raise_for_status()
                results[f"source_{i+1}"] = response.json()
            except httpx.RequestError as e:
                results[f"source_{i+1}"] = {"error": str(e)}
            except httpx.HTTPStatusError as e:
                results[f"source_{i+1}"] = {"error": f"HTTP error: {e.response.status_code}"}
    return results
