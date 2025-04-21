import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

# 방탈출 예약 페이지 URL
url = os.getenv("URL")

# Pushover 설정
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

def check_reservation():
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    buttons = soup.select('.res-times-btn label')
    for btn in buttons:
        if '예약가능' in btn.text:
            print("예약 가능 시간 발견!")
            return True
    return False

def send_notification():
    print("푸시 알림 전송 중...")
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": "🎉 방탈출 예약 가능해졌어요! 어서 잡으세요!"
    })

# 주기적으로 확인 (1분마다)
while True:
    if check_reservation():
        send_notification()
        break
    print("아직 예약 불가. 다시 확인 예정...")
    time.sleep(60)
