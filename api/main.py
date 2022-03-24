from fastapi import FastAPI

app = FastAPI()


@app.get("/stats/{date}")
async def root(date: str):
    return {"message": date }
