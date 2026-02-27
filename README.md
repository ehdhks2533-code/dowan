# 통합 대시보드 (Integrated Dashboard)

로컬, 휴대폰, 아이패드에서 접속 가능한 통합 대시보드입니다. 시스템 프로세스와 커스텀 Python/Node.js 스크립트를 모니터링하고 제어할 수 있습니다.

## 기능

- 📊 **시스템 모니터링**: CPU, 메모리, 디스크 사용률 실시간 모니터링
- 🔧 **서비스 관리**: 커스텀 스크립트 시작/중지/재시작
- 📝 **로그 뷰어**: 서비스별 실시간 로그 확인
- 📱 **원격 접속**: 로컬, 휴대폰, 아이패드에서 접속 가능
- 🔐 **인증**: 토큰 기반 보안 인증

## 설치 및 실행

### 1. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 대시보드 실행

```bash
python app.py
```

기본 설정:
- **주소**: http://localhost:5000
- **기본 비밀번호**: `admin123` (config.py에서 변경 가능)

### 3. 원격 접속 (휴대폰, 아이패드)

1. PC의 IP 주소 확인:
   ```bash
   # Linux/Mac
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

2. 휴대폰/아이패드에서 접속:
   ```
   http://<PC의 IP주소>:5000
   ```

## 서비스 추가하기

### config.py에서 서비스 등록

```python
SERVICES = {
    'my_service': {
        'name': '내 서비스',
        'description': '서비스 설명',
        'command': 'python my_script.py',  # 실행할 명령어
        'auto_restart': True,
        'enabled': True,
    },
    'another_service': {
        'name': '다른 서비스',
        'description': '또 다른 서비스',
        'command': 'node my_app.js',
        'auto_restart': False,
        'enabled': True,
    },
}
```

## 프로젝트 구조

```
dowan/
├── app.py                      # Flask 메인 애플리케이션
├── config.py                   # 설정 파일
├── requirements.txt            # Python 의존성
├── auth/                       # 인증 모듈
│   ├── __init__.py
│   └── auth.py                 # JWT 토큰 관리
├── services/                   # 서비스 관리 모듈
│   ├── __init__.py
│   ├── process_manager.py      # 프로세스 제어
│   ├── log_manager.py          # 로그 관리
│   └── system_monitor.py       # 시스템 모니터링
├── api/                        # REST API 엔드포인트
│   ├── __init__.py
│   ├── auth.py                 # 인증 API
│   ├── services.py             # 서비스 관리 API
│   ├── logs.py                 # 로그 API
│   └── status.py               # 상태 조회 API
├── static/                     # 웹 프론트엔드
│   ├── index.html              # 메인 페이지
│   ├── css/
│   │   └── style.css           # 스타일시트
│   └── js/
│       ├── api.js              # API 통신 모듈
│       └── dashboard.js        # 대시보드 스크립트
├── logs/                       # 서비스 로그 저장소
└── data/                       # 데이터 저장소
```

## API 엔드포인트

### 인증
- `POST /api/auth/login` - 로그인
- `POST /api/auth/logout` - 로그아웃
- `GET /api/auth/verify` - 토큰 검증

### 서비스 관리
- `GET /api/services` - 모든 서비스 조회
- `GET /api/services/<service_id>` - 특정 서비스 조회
- `POST /api/services/<service_id>/start` - 서비스 시작
- `POST /api/services/<service_id>/stop` - 서비스 중지
- `POST /api/services/<service_id>/restart` - 서비스 재시작

### 로그 관리
- `GET /api/logs/<service_id>` - 로그 조회
- `POST /api/logs/<service_id>/clear` - 로그 초기화
- `GET /api/logs/<service_id>/size` - 로그 파일 크기

### 상태 조회
- `GET /api/status/system` - 시스템 상태
- `GET /api/status/dashboard` - 대시보드 전체 상태

## 설정 변경

### config.py

```python
# 기본 비밀번호 변경 (환경 변수 권장)
DEFAULT_PASSWORD = 'your-secure-password'

# 서버 주소/포트 변경
HOST = '0.0.0.0'  # 모든 IP에서 접속 가능
PORT = 5000

# 조직화 및 보안
SECRET_KEY = 'your-secret-key'
JWT_SECRET_KEY = 'your-jwt-secret-key'
```

### 환경 변수 사용 (권장)

```bash
export DASHBOARD_PASSWORD='your-secure-password'
export SECRET_KEY='your-secret-key'
export JWT_SECRET_KEY='your-jwt-secret-key'
python app.py
```

## 보안 주의사항

⚠️ **프로덕션 배포 전 반드시 다음을 확인하세요:**

1. **비밀번호 변경**: `config.py`의 기본 비밀번호를 강력한 비밀번호로 변경
2. **HTTPS 설정**: 원격 접속 시 HTTPS 사용 권장
3. **JWT 비밀키 변경**: 기본값이 아닌 강력한 비밀키 사용
4. **방화벽 설정**: 필요한 포트만 개방
5. **접근 제어**: 신뢰할 수 있는 네트워크에서만 접속

## 테스트

### 샘플 서비스 실행

```bash
# config.py의 sample_service로 이미 등록되어 있음
# 대시보드에서 "Sample Service" 시작 버튼을 클릭
```

### 커스텀 서비스 추가 및 테스트

1. Python 스크립트 생성:
```python
# my_test_script.py
import time
while True:
    print(f"[INFO] 현재 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(2)
```

2. config.py에서 서비스 등록:
```python
SERVICES = {
    'test_service': {
        'name': '테스트 서비스',
        'description': '테스트용 Python 스크립트',
        'command': 'python my_test_script.py',
        'auto_restart': True,
        'enabled': True,
    },
}
```

3. 대시보드에서 서비스 시작/중지 테스트

## 문제 해결

### 1. 포트 이미 사용 중
```bash
# 다른 포트로 실행
PORT=8080 python app.py
```

### 2. 권한 부족 (서비스 시작 실패)
```bash
# 관리자 권한으로 실행
sudo python app.py
```

### 3. 원격 접속 실패
- PC와 휴대폰이 같은 네트워크에 연결되었는지 확인
- PC의 방화벽 설정 확인
- PC의 IP 주소가 올바른지 확인

## 라이센스

MIT License

## 기여하기

버그 보고 및 기능 제안은 언제든 환영합니다!
