from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import pprint

app = FastAPI()

@app.post("/")
async def feishu_event(request: Request):
    body = await request.json()
    pprint.pprint(body)
    print("Received body:", body)

    if "challenge" in body:
        # Required for Feishu verification
        return JSONResponse(content={"challenge": body["challenge"]})

    # Normal event
    return JSONResponse(content={"code": 0})
