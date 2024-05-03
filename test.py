import pymongo

# MongoDB 연결 정보
mongo_host = 'localhost'  # 또는 컨테이너의 IP 주소
mongo_port = 27017
mongo_user = 'admin'
mongo_password = '2024md'

# MongoDB에 연결
try:
    client = pymongo.MongoClient(f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}')
    db = client.admin  # 연결 테스트를 위해 admin 데이터베이스 사용
    print("Connected to MongoDB successfully!")
except pymongo.errors.ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
finally:
    if 'client' in locals():
        client.close()
