## 프로젝트 실행 방법
### 1. 깃허브 클론
`https://github.com/2024-Mirim-Dancing/dancing-back.git`
<br>

### 2. Docker desktop 설치 후 로그인
[docker 공식사이트](https://www.docker.com/products/docker-desktop/) 에서 Docker descktop을 설치 후
터미널에 `docker login`을 입력하여 로그인합니다.
<br>

### 3. Docker Compose 빌드
방금 전 클론 받은 파일에 들어가서 터미널에서 Dockerfile이 있는 디렉토리로 이동한 후 다음 명령을 실행하여 Docker 이미지를 빌드합니다.
```bash
docker-compose build
```

### 4. Docker Compose 실행
Docker Compose를 사용하여 애플리케이션을 실행합니다. 이 명령은 컨테이너를 생성하고 시작합니다.

```bash
docker-compose up -d
```

<br>

## API 명세서
- [API 명세서](https://github.com/2024-Mirim-Dancing/Dancing_Back/wiki/API-%EB%AA%85%EC%84%B8%EC%84%9C)
- Swagger `/docs`
