# 통합 대시보드 - 빠른 시작 가이드

## 설치 및 실행 (1분)

### 1단계: 패키지 설치
```bash
pip install -r requirements.txt
```

### 2단계: 대시보드 실행
```bash
python app.py
```

기본 주소: `http://localhost:5000`
기본 비밀번호: `admin123`

## 로컬에서 접속
- 브라우저에서 `http://localhost:5000` 접속
- 비밀번호 입력: `admin123`

## 원격에서 접속 (휴대폰/아이패드)

### 1. PC의 IP 주소 확인
```bash
# Linux/Mac
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows PowerShell
ipconfig
```

### 2. 휴대폰/아이패드에서 접속
```
http://<PC의 IP>:5000
```

예: `http://192.168.1.100:5000`

## 서비스 추가하기

### config.py 수정
```python
SERVICES = {
    'my_service': {
        'name': '내 서비스',
        'description': '서비스 설명',
        'command': 'python my_script.py',  # 실행할 명령어
        'auto_restart': True,
        'enabled': True,
    },
}
```

### 지원되는 명령어
- Python: `python my_script.py`
- Node.js: `node my_app.js`
- Shell: `bash my_script.sh`
- 커스텀: 실행 가능한 모든 명령어

## 주요 기능

### 대시보드
- ✅ CPU, 메모리, 디스크 사용률 실시간 모니터링
- ✅ 서비스 상태 확인 (실행/중지)
- ✅ 프로세스 정보 (PID, CPU, 메모리)
- ✅ 자동 새로고침 (2초마다)

### 서비스 관리
- ✅ 서비스 시작
- ✅ 서비스 중지
- ✅ 서비스 재시작
- ✅ 상태 확인

### 로그 뷰어
- ✅ 실시간 로그 확인
- ✅ 서비스별 로그 필터링
- ✅ 로그 초기화

## 테스트하기

### 샘플 서비스 실행
```bash
# 대시보드에서 "Sample Service" 시작 버튼 클릭
# 또는 API로:
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"admin123"}' | python -c "import sys, json; print(json.load(sys.stdin)['token'])")

curl -X POST http://localhost:5000/api/services/sample_service/start \
  -H "Authorization: Bearer $TOKEN"
```

## 비밀번호 변경

### 환경 변수로 변경 (권장)
```bash
export DASHBOARD_PASSWORD='your-secure-password'
python app.py
```

### config.py에서 변경
```python
DEFAULT_PASSWORD = 'your-secure-password'
```

## 문제 해결

### 포트가 이미 사용 중인 경우
```bash
PORT=8080 python app.py
# 그 후 http://localhost:8080 접속
```

### 권한 부족 (서비스 시작 실패)
```bash
sudo python app.py
```

### 원격 접속 불가
1. PC와 휴대폰이 같은 네트워크에 연결되었는지 확인
2. PC의 방화벽에서 5000번 포트 허용
3. 올바른 IP 주소 사용 확인

## API 사용법

### 로그인
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"admin123"}'
```

응답:
```json
{
  "success": true,
  "token": "your-token-here",
  "message": "로그인 성공"
}
```

### 모든 서비스 조회
```bash
TOKEN="your-token"
curl -X GET http://localhost:5000/api/services \
  -H "Authorization: Bearer $TOKEN"
```

### 서비스 시작
```bash
curl -X POST http://localhost:5000/api/services/sample_service/start \
  -H "Authorization: Bearer $TOKEN"
```

### 서비스 중지
```bash
curl -X POST http://localhost:5000/api/services/sample_service/stop \
  -H "Authorization: Bearer $TOKEN"
```

### 로그 조회
```bash
curl -X GET "http://localhost:5000/api/logs/sample_service?limit=100" \
  -H "Authorization: Bearer $TOKEN"
```

## 프로덕션 배포

### 1. WSGI 서버 사용 (gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. HTTPS 설정 (nginx + Let's Encrypt)
- 참고: README.md 보안 섹션

### 3. 데이터베이스 마이그레이션
- 현재는 인메모리 토큰 저장소 사용
- 프로덕션에서는 데이터베이스로 변경 권장

## 더 많은 정보
자세한 내용은 README.md를 참고하세요.
