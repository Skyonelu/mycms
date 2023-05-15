import asyncio
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def root():
    return {"message": "Hello World"}

@app.get("/1")
async def root():
    await asyncio.sleep(10)
    return {"message": "Hello World"}

@app.get("/2")
def root():
    time.sleep(10)

    return {"message": "Hello World"}
@app.get("/3")
def root():
    time.sleep(10)

    return {"message": "Hello World"}

@app.get("/4")
def root():

    return {"message": "Hello World"}

if __name__ == "__main__":
    print("Hello World")
    uvicorn.run(app='main:app', host="0.0.0.0", port=8080, reload=True, workers=4)
