from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from enum import Enum
import os
from urllib.parse import quote, unquote

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000"   # Alternative local address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 연결
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI 환경 변수가 설정되지 않았습니다.")
client = MongoClient(mongo_uri)
db = client["admin"]
user_collection = db["user"]

# 선생님 열거형 정의
class Teacher(str, Enum):
    KYH = "KYH"
    YBS = "YBS"
    KJS = "KJS"
    KYC = "KYC"
    KHS = "KHS"
    SMS = "SMS"

@app.get("/")
async def index():
    return "home"

@app.post("/score/{user_id}/{score}/{teacher}", tags=["score"])
async def submit_score(user_id: str = Path(..., title="사용자 ID", description="사용자의 고유한 ID"),
                       score: int = Path(..., title="점수", description="점수"),
                       teacher: Teacher = Path(..., title="선생님", description="점수를 부여한 선생님")):
    """
    사용자의 점수를 제출합니다.

    - **user_id**: 사용자의 고유한 ID입니다.
    - **score**: 제출할 점수입니다.
    - **teacher**: 점수를 부여한 선생님입니다.
    """
    # 사용자 아이디와 선생님 이름을 URL 인코딩
    user_id_encoded = quote(user_id)
    teacher_encoded = quote(teacher.value)

    # 사용자 아이디로 검색 후 결과가 없으면 새로운 사용자 추가
    existing_user = user_collection.find_one({"user_id": user_id_encoded})
    if not existing_user:
        user_collection.insert_one({"user_id": user_id_encoded, "score": score, "teacher": teacher_encoded})
    else:
        # 이미 존재하는 사용자의 경우 기존 점수와 비교하여 업데이트
        if score > existing_user["score"]:
            user_collection.update_one({"user_id": user_id_encoded}, {"$set": {"score": score, "teacher": teacher_encoded}})

    return JSONResponse(content={"message": "Score submitted successfully"})

@app.get("/ranking", tags=["ranking"])
async def get_ranking():
    """
    사용자의 랭킹을 가져옵니다.
    """
    ranking = list(user_collection.find(projection={"_id": 0}).sort("score", -1))
    # 사용자 ID와 선생님 이름을 URL 디코딩하여 원래의 값으로 변환
    for user in ranking:
        user["user_id"] = unquote(user["user_id"])
        if "teacher" in user:
            user["teacher"] = unquote(user["teacher"])
    return JSONResponse(content={"ranking": ranking})
