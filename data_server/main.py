from fastapi import FastAPI, Query, HTTPException
from search import setup_redis, search_music_data, push_data
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_redis()
    yield

@app.get("/search")
async def search(query: str = Query(..., description="검색할 곡 이름 또는 키워드")):
    try:
        result = await search_music_data(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/new")
async def get_new(v_id: str = Query(..., description="가져올 곡 영상 ID")):
    try:
        result = await push_data(v_id)
        url = result['url']
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))