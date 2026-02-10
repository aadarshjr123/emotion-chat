import os, sys, httpx
from app.core.config import settings


async def analyze_emotion(text: str) -> str:
    if not text.strip():
        return "neutral"

    headers = (
        {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}
        if settings.HF_API_TOKEN
        else {}
    )
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                settings.MODEL_URL, headers=headers, json={"inputs": text}
            )
            data = resp.json()

            if isinstance(data, dict) and "error" in data:
                print("HF error:", data["error"], flush=True)
                return "neutral"

            if not isinstance(data, list) or not data:
                return "neutral"

            top = max(data[0], key=lambda x: x.get("score", 0))
            label = top.get("label", "").lower()
            if "pos" in label:
                return "positive"
            elif "neg" in label:
                return "negative"
            return "neutral"
    except Exception as e:
        print("HF Exception:", e, flush=True)
        return "neutral"
