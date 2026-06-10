import io
import httpx

async def generate_code_image(code_text: str, theme: str = "monokai"):
    
    api_endpoints = [
        "https://carbonara.solopov.dev/api/cook",
        "https://carbonara.vercel.app/api/cook",
        "https://carbon-api.vercel.app/api",
        "https://code-to-image.vercel.app/api/cook"
    ]
    
    payload = {
        "code": code_text,
        "backgroundColor": "#1F1F24",
        "theme": theme,
        "exportSize": "2x",
        "paddingVertical": "30px",
        "paddingHorizontal": "30px"
    }
    
    print(f"🎨 [RENDERER] Starting API Roulette... (Snippet Length: {len(code_text)})")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for api_url in api_endpoints:
            try:
                print(f"🔄 [ROULETTE] Attempting connection to: {api_url}")
                response = await client.post(api_url, json=payload)
                
                if response.status_code == 200:
                    print(f"✅ [SUCCESS] Bypassed firewall! Image rendered via {api_url}")
                    
                    img_buffer = io.BytesIO(response.content)
                    img_buffer.name = "snippet.png" 
                    return img_buffer
                else:
                    print(f"⚠️ [BLOCKED] {api_url} rejected the server (Status: {response.status_code}).")
                    
            except Exception as e:
                print(f"⚠️ [TIMEOUT/ERROR] {api_url} failed to respond: {e}")
                continue

    print("❌ [CRITICAL] All API endpoints in the roulette blocked the server.")
    return None