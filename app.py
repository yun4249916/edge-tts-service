import io
import edge_tts
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI(title="Edge TTS Service")
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

@app.get("/")
def health():
    return {"ok": True, "service": "edge-tts-service"}

@app.get("/voices")
async def voices():
    vs = await edge_tts.list_voices()
    zh = [v for v in vs if v["Locale"].startswith("zh")]
    return {"count": len(zh), "voices": [{"ShortName": v["ShortName"], "Gender": v["Gender"], "Locale": v["Locale"]} for v in zh]}

@app.get("/tts")
async def tts(text: str = Query(...), voice: str = Query(DEFAULT_VOICE), rate: str = Query("+0%"), pitch: str = Query("+0Hz")):
    buf = io.BytesIO()
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    buf.seek(0)
    return StreamingResponse(buf, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=tts.mp3"})
