import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BRS_API_KEY")

async def get_market_data():
    gold_url = f"https://Api.BrsApi.ir/Market/Gold_Currency.php?key={API_KEY}"
    commodity_url = f"https://Api.BrsApi.ir/Market/Commodity.php?key={API_KEY}"
    
    results = {
        "usd": None,
        "eur": None,
        "gold_18k": None,
        "silver_ounce": None
    }

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Fetch Gold & Currency
            async with session.get(gold_url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract USD
                    for item in data.get("currency", []):
                        if item["symbol"] == "USD":
                            results["usd"] = f"{item['price']:,} {item['unit']}"
                            break
                    
                    # Extract EUR
                    for item in data.get("currency", []):
                        if item["symbol"] == "EUR":
                            results["eur"] = f"{item['price']:,} {item['unit']}"
                            break
                    
                    # Extract 18k Gold
                    for item in data.get("gold", []):
                        if item["symbol"] == "IR_GOLD_18K":
                            results["gold_18k"] = f"{item['price']:,} {item['unit']}"
                            break

            # 2. Fetch Commodities (for Silver)
            async with session.get(commodity_url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract Silver (XAGUSD)
                    for item in data.get("metal_precious", []):
                        if item["symbol"] == "XAGUSD":
                            results["silver_ounce"] = f"{item['price']:,} {item['unit']}"
                            break
                            
            return results

        except Exception as e:
            print(f"API Error: {e}")
            return None

if __name__ == "__main__":
    async def test_api():
        print("Fetching specific prices...")
        data = await get_market_data()
        print(data)
        
    asyncio.run(test_api())