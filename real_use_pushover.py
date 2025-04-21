import requests
from bs4 import BeautifulSoup
import time
import datetime
import schedule
from dotenv import load_dotenv
import os

load_dotenv()

# 방탈출 예약 페이지 URL
url = os.getenv("URL")

# Pushover 설정
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

# 최근 알림 시간 저장 (중복 방지용)
last_alert_time = None

def send_pushover_notification(title, message, priority=0):
    """Pushover로 알림 보내기"""
    try:
        data = {
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
            "priority": priority,
            "sound": "magic"
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=data)
        if response.status_code == 200:
            print(f"[{datetime.datetime.now()}] Pushover 알림 전송 성공!")
        else:
            print(f"[{datetime.datetime.now()}] Pushover 알림 실패: {response.text}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 알림 오류: {e}")

def check_availability():
    global last_alert_time
    now = datetime.datetime.now()
    print(f"[{now}] 빈자리 확인 중...")

    # 최근 알림 이후 30분 이내면 생략
    if last_alert_time and (now - last_alert_time).total_seconds() < 1800:
        print(f"[{now}] 최근 알림 후 30분 미만 → 생략")
        return False

    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 버튼 목록 가져오기
        buttons = soup.select('.res-times-btn button')
        available_times = []

        for button in buttons:
            label = button.select_one('label')
            span = button.select_one('span')

            # 예약불가 텍스트가 아니면 예약 가능으로 간주
            if label and '예약불가' not in label.text:
                time_text = span.text.strip() if span else "(시간 없음)"
                available_times.append(time_text)

        if available_times:
            print(f"[{now}] 예약 가능 시간 발견! {', '.join(available_times)}")
            send_pushover_notification(
                "🎮 25일 방탈출 빈자리 알림!",
                f"[{now.strftime('%H:%M:%S')}] 예약 가능한 시간대: {', '.join(available_times)}\n\n예약 링크: {url}",
                priority=1
            )
            last_alert_time = now
        else:
            print(f"[{now}] 현재 예약 가능한 시간대가 없습니다.")

    except Exception as e:
        print(f"[{datetime.datetime.now()}] 오류 발생: {e}")
        send_pushover_notification("방탈출 알리미 오류", f"오류 발생: {e}", priority=0)

def main():
    print("🚀 방탈출 빈자리 알림 프로그램 시작")
    print(f"🔍 모니터링 URL: {url}")

    # 시작 알림
    send_pushover_notification("방탈출 알리미 시작", "방탈출 빈자리 알림 프로그램이 시작되었습니다.")

    # 처음 한 번 실행
    check_availability()

    # 이후 3분마다 반복
    schedule.every(3).minutes.do(check_availability)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
