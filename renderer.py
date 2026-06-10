import io
import httpx

async def generate_code_image(code_text: str, theme: str = "monokai"):
    try:
        api_url = "https://carbonara.solopov.dev/api/cook"
        
        payload = {
            "code": code_text,
            "backgroundColor": "#1F1F24",
            "theme": theme,
            "exportSize": "2x",
            "paddingVertical": "30px",
            "paddingHorizontal": "30px"
        }
        
        print(f"🎨 [RENDERER] Sending snippet to API... (Length: {len(code_text)} characters)")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, json=payload)
        
        if response.status_code == 200:
            print("✅ [RENDERER] API successfully generated the image!")
            
            img_buffer = io.BytesIO(response.content)
            img_buffer.name = "snippet.png" 
            return img_buffer
            
        else:
            print(f"❌ [API ERROR] Status Code: {response.status_code}")
            print(f"❌ [API RESPONSE TEXT]: {response.text}") 
            return None
            
    except Exception as e:
        print(f"⚠️ [CRITICAL RENDERER EXCEPTION]: {e}")
        return None