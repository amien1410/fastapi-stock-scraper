import httpx
from utils.cnn_processors import (
    extract_stock_info,
    calculate_price_change_summary,
    calculate_price_momentum
)

CNN_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,id;q=0.8,fa;q=0.7,ar;q=0.6,ms;q=0.5,ja;q=0.4,es;q=0.3",
    "origin": "https://edition.cnn.com",
    "priority": "u=1, i",
    "referer": "https://edition.cnn.com/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    )
}

async def one_year_prices(ticker: str):
    url = f"https://production.dataviz.cnn.io/charting/instruments/{ticker.upper()}/1Y/false"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(url, headers=CNN_HEADERS)
            response.raise_for_status()
            raw_data = response.json()
            return {
                "symbol": ticker.upper(),
                "change_summary": calculate_price_change_summary(raw_data),
                "price_momentum": calculate_price_momentum(raw_data)
            }
        except httpx.RequestError as e:
            return {"error": str(e)}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP status error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}

async def five_competitors(ticker: str):
    url = f"https://production.dataviz.cnn.io/quote/competitors/{ticker.upper()}/5"
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(url, headers=CNN_HEADERS)
            response.raise_for_status()
            raw_data = response.json()
            return extract_stock_info(raw_data)
        except httpx.RequestError as e:
            return {"error": str(e)}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP status error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
            
# BACKUP

# async def one_year_prices(ticker: str):
#     url = f"https://production.dataviz.cnn.io/charting/instruments/{ticker.upper()}/1Y/false"
#     async with httpx.AsyncClient(timeout=10) as client:
#         try:
#             response = await client.get(url, headers=CNN_HEADERS)
#             response.raise_for_status()
#             return response.json()
#         except httpx.RequestError as e:
#             return {"error": str(e)}
#         except httpx.HTTPStatusError as e:
#             return {"error": f"HTTP status error: {e.response.status_code}"}

# async def five_competitors(ticker: str):
#     url = f"https://production.dataviz.cnn.io/quote/competitors/{ticker.upper()}/5"
#     async with httpx.AsyncClient(timeout=10) as client:
#         try:
#             response = await client.get(url, headers=CNN_HEADERS)
#             response.raise_for_status()
#             return response.json()
#         except httpx.RequestError as e:
#             return {"error": str(e)}
#         except httpx.HTTPStatusError as e:
#             return {"error": f"HTTP status error: {e.response.status_code}"}
