from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import os

app = FastAPI()

# MongoDB 연결
mongo_uri = os.getenv("MONGO_URI")  # 환경 변수에서 URI 가져오기
client = MongoClient(mongo_uri)
db = client["admin"]
user_collection = db["user"]

@app.get("/")
async def index():
    return "home"

@app.post("/score/{user_id}/{score}", tags=["score"])
async def submit_score(user_id: str = Path(..., title="사용자 ID", description="사용자의 고유한 ID"),
                       score: int = Path(..., title="점수", description="점수")):
    """
    사용자의 점수를 제출합니다.

    - **user_id**: 사용자의 고유한 ID입니다.
    - **score**: 제출할 점수입니다.
    """
    # 사용자 아이디로 검색 후 결과가 없으면 새로운 사용자 추가
    existing_user = user_collection.find_one({"user_id": user_id})
    if not existing_user:
        user_collection.insert_one({"user_id": user_id, "score": score})
    else:
        # 이미 존재하는 사용자의 경우 기존 점수와 비교하여 업데이트
        if score > existing_user["score"]:
            user_collection.update_one({"user_id": user_id}, {"$set": {"score": score}})

    return JSONResponse(content={"message": "Score submitted successfully"})

@app.get("/ranking", tags=["ranking"])
async def get_ranking():
    """
    사용자의 랭킹을 가져옵니다.
    """
    ranking = list(user_collection.find(projection={"_id": 0}).sort("score", -1))
    return JSONResponse(content={"ranking": ranking})
