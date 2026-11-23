import json
from fastapi.responses import StreamingResponse

def event_stream(payload: dict):
    async def generate():
        message = json.dumps(payload)
        yield f"event: message\ndata: {message}\n\n"
        yield "event: done\ndata: {}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
