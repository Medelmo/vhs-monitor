from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.vhs-bamberg.de/p/502-CAT-KAT4576046"

TARGET_DATE_STRINGS = [
    "06.2026",
    "07.2026",
    "08.2026",
    "09.2026",
    "10.2026",
    "11.2026"
]

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(api_url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

    print(response.text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    content = page.content()

    found_dates = []

    for date_string in TARGET_DATE_STRINGS:
        if date_string in content:
            found_dates.append(date_string)

    browser.close()

if found_dates:
    message = (
        "VHS Bamberg Update Detected!\n\n"
        f"Found dates: {', '.join(found_dates)}\n\n"
        f"{URL}"
    )

    send_telegram(message)

    print("Notification sent.")
else:
    print("No new months found.")
