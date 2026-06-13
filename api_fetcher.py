import aiohttp
import asyncio

async def get_market_data():
    FIAT_URL = "https://raw.githubusercontent.com/meytiii/sarraf-bashi-bot/main/data/fiat.json"
    GOLD_URL = "https://raw.githubusercontent.com/meytiii/sarraf-bashi-bot/main/data/gold.json"
    
    results = {
        "usd": "نامشخص",
        "eur": "نامشخص",
        "gbp": "نامشخص",
        "gold_18k": "نامشخص",
        "silver_ounce": "نامشخص"
    }

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=timeout) as session:
        try:
            async with session.get(FIAT_URL) as response:
                if response.status == 200:
                    fiat_data = await response.json(content_type=None)
                    
                    if "usd" in fiat_data:
                        results["usd"] = f"{int(fiat_data['usd']['value']):,} تومان"
                    if "eur" in fiat_data:
                        results["eur"] = f"{int(fiat_data['eur']['value']):,} تومان"
                    if "gbp" in fiat_data:
                        results["gbp"] = f"{int(fiat_data['gbp']['value']):,} تومان"
            
            async with session.get(GOLD_URL) as response:
                if response.status == 200:
                    gold_data = await response.json(content_type=None)
                    
                    if "18ayar" in gold_data:
                        results["gold_18k"] = f"{int(gold_data['18ayar']['value']):,} تومان"
            
            async with session.get(FIAT_URL) as response:
                if response.status == 200:
                    fiat_data = await response.json(content_type=None)
                    if "xag" in fiat_data:
                        results["silver_ounce"] = f"{int(fiat_data['xag']['value']):,} دلار" 

            return results

        except Exception as e:
            print(f"🚨 GitHub Fetch Error: {e}")
            return None