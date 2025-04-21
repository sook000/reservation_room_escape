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

def send_pushover_notification(title, message, priority=0):
    """Pushover로 알림 보내기"""
    try:
        data = {
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
            "priority": priority,  # -2 to 2: -2 (lowest), -1 (low), 0 (normal), 1 (high), 2 (emergency)
            "sound": "magic"  # 알림음 설정: https://pushover.net/api#sounds
        }
        
        response = requests.post("https://api.pushover.net/1/messages.json", data=data)
        if response.status_code == 200:
            print(f"[{datetime.datetime.now()}] Pushover 알림 전송 성공!")
            return True
        else:
            print(f"[{datetime.datetime.now()}] Pushover 알림 전송 실패: {response.text}")
            return False
            
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Pushover 알림 전송 중 오류: {e}")
        return False

def check_availability():
    print(f"[{datetime.datetime.now()}] 빈자리 확인 중...")
    try:
        # 웹페이지 가져오기
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        response.raise_for_status()  # 요청 실패시 예외 발생
        
        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 예약 가능한 시간대 버튼 찾기 - 보다 정확한 CSS 선택자 사용
        # # .res-times-btn 클래스를 가진 div 안의 button 요소들
        # buttons = soup.select('.res-times-btn button')

        # available_times = []
        # for button in buttons:
        #     label = button.select_one('label')
        #     span = button.select_one('span')

        #     # 예약불가 라벨이 없을 경우만 추가
        #     if label and '예약불가' not in label.text:
        #         if span and span.text.strip():
        #             available_times.append(span.text.strip())
        #         elif button.text.strip():
        #             available_times.append(button.text.strip())
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
            print(f"[{datetime.datetime.now()}] 빈자리 발견! {', '.join(available_times)}")
            
            # Pushover로 알림 보내기 (우선순위 1: 높음)
            send_pushover_notification(
                "🎮 방탈출 빈자리 알림!", 
                f"예약 가능한 시간대: {', '.join(available_times)}\n\n예약 링크: {url}",
                priority=1
            )
            
            # 빈자리를 찾았다면 알림을 더 자주 보내지 않기 위해 30분간 대기
            time.sleep(1800)  # 30분(1800초) 대기
            return True
        
        print(f"[{datetime.datetime.now()}] 현재 예약 가능한 시간대가 없습니다.")
        return False
            
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 오류 발생: {e}")
        send_pushover_notification("방탈출 알리미 오류", f"프로그램 실행 중 오류 발생: {e}", priority=0)
        return False

def main():
    print("방탈출 빈자리 알림 프로그램이 시작되었습니다.")
    print(f"모니터링 중인 URL: {url}")
    
    # 프로그램 시작 알림
    send_pushover_notification("방탈출 알리미 시작", "방탈출 빈자리 알림 프로그램이 시작되었습니다.")
    
    # 초기 체크
    check_availability()
    
    # 3분마다 체크하도록 스케줄링
    schedule.every(3).minutes.do(check_availability)
    
    # 스케줄 실행
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()