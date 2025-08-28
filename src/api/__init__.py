from typing import Union
import asyncio
import time

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/events")
async def stream_events():
    async def event_stream():
        count = 0
        while True:
            yield f"yo"
            count += 1
            await asyncio.sleep(1)

    return StreamingResponse(event_stream(), media_type="text/plain")


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
