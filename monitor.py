from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.vhs-bamberg.de/p/502-CAT-KAT4576046"

TARGET_MONTHS = [
    "Juli",
    "August",
    "September",
    "Oktober",
    "November"
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

    found_months = []

    for month in TARGET_MONTHS:
        if month in content:
            found_months.append(month)

    browser.close()

if found_months:
    message = (
        "VHS Bamberg Update Detected!

"
        f"Found months: {', '.join(found_months)}

"
        f"{URL}"
    )

    send_telegram(message)

    print("Notification sent.")
else:
    print("No new months found.")
