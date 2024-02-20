from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

app = FastAPI()

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["admin"]
user_collection = db["user"]

@app.post("/score/{user_id}/{score}")
async def submit_score(user_id: str, score: int):
    # 사용자 아이디로 검색 후 결과가 없으면 새로운 사용자 추가
    existing_user = user_collection.find_one({"user_id": user_id})
    if not existing_user:
        user_collection.insert_one({"user_id": user_id, "score": score})
    else:
        # 이미 존재하는 사용자의 경우 기존 점수와 비교하여 업데이트
        if score > existing_user["score"]:
            user_collection.update_one({"user_id": user_id}, {"$set": {"score": score}})

    return JSONResponse(content={"message": "Score submitted successfully"})

@app.get("/ranking")
async def get_ranking():
    ranking = list(user_collection.find(projection={"_id": 0}).sort("score", -1))
    return JSONResponse(content={"ranking": ranking})

