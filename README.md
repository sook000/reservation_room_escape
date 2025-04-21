# 🧩 방탈출 예약 알림 봇

방탈출 예약 페이지를 자동으로 모니터링하고, 예약 가능 시간이 생기면  
[Pushover](https://pushover.net) 푸시 알림으로 즉시 알려주는 파이썬 스크립트입니다.

✅ 실제로 이 알림 덕분에 취소된 시간을 예약하는 데 성공했습니다!

---

## 📌 주요 기능

- 예약 페이지에서 예약 가능 시간 자동 감지
- 예약 가능 시 푸시 알림 전송 (Pushover 사용)
- 3분 간격 자동 체크
- 최근 30분 이내 알림 중복 방지

---

## 🛠️ 실행 방법

### 1. 저장소 클론

### 2. 필수 라이브러리 설치

```
pip install -r requirements.txt
```

### 3. 환경 변수 설정

.env.example 파일을 참고하여 .env 파일을 만드세요. 방탈출 예약 URL, Pushover 키, API 토큰 정보를 입력하세요.

```
# .env
URL=https://example.com/your-reservation-url
PUSHOVER_USER_KEY=your-pushover-user-key
PUSHOVER_API_TOKEN=your-pushover-api-token
```

#### 🔐 Pushover 설정 방법

1. [Pushover](https://pushover.net) 사이트에서 회원가입
2. 앱 등록 후 Application Token 생성 (최초 30일 무료)
3. 자신의 User Key 확인
4. .env 파일에 키 값 입력

### 4. 실행

```
python real_use_pushover.py
```

- 실제 방탈출 취소를 잡는 데 사용했던 파일은 real_use_pushover.py 입니다
- 프로그램 시작 시 → 방탈출 알리미 시작 알림 전송
- 이후 3분마다 예약 가능 여부 확인
- 예약 가능 시간이 발견되면 푸시 알림 전송

---

### ✅ 예시 알림 메시지

#### 프로그램 시작 시

```
방탈출 알리미 시작
방탈출 빈자리 알림 프로그램이 시작되었습니다.
```

#### 예약 가능 시간 발견할 때

```
🎮 25일 방탈출 빈자리 알림!
[13:55:01] 예약 가능한 시간대: 15:10, 16:25
예약 링크: https://example.com/your-reservation-url
```
