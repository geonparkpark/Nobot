import httpx
import os

DATA_SERVER_URL = os.getenv("DATA_SERVER_URL", "http://localhost:8000")

    # 데이터 요청 -> 데이터 서버
async def search_data(query: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_SERVER_URL}/search", params={"query": query})
        res.raise_for_status()
        return res.json()

async def get_new_data(query: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{DATA_SERVER_URL}/new", params={"query": query})
        res.raise_for_status()
        return res.json()