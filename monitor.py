from playwright.sync_api import sync_playwright
import requests
import os

URL = "https://www.vhs-bamberg.de/p/502-CAT-KAT4576046"

TARGET_DATE_STRINGS = [
    "08.2026",
    "09.2026",
    "10.2026",
    "11.2026",
    "12.2026"
]

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
EMAIL_SMTP_PORT = os.getenv("EMAIL_SMTP_PORT")
EMAIL_SMTP_USER = os.getenv("EMAIL_SMTP_USER")
EMAIL_SMTP_PASSWORD = os.getenv("EMAIL_SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram config missing; skipping Telegram notification.")
        return

    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(api_url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

    print(response.text)


def send_email(message, subject="VHS Bamberg Update Detected"):
    if not (EMAIL_SMTP_HOST and EMAIL_SMTP_PORT and EMAIL_SMTP_USER and EMAIL_SMTP_PASSWORD and EMAIL_FROM and EMAIL_TO):
        print("Email config incomplete; skipping email notification.")
        return

    try:
        smtp_port = int(EMAIL_SMTP_PORT)
    except ValueError:
        print(f"Invalid EMAIL_SMTP_PORT: {EMAIL_SMTP_PORT}; skipping email notification.")
        return

    from email.message import EmailMessage
    import smtplib
    import ssl

    email_message = EmailMessage()
    email_message["Subject"] = subject
    email_message["From"] = EMAIL_FROM
    email_message["To"] = EMAIL_TO
    email_message.set_content(message)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(EMAIL_SMTP_HOST, smtp_port) as server:
            server.starttls(context=context)
            server.login(EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD)
            server.send_message(email_message)
        print("Email notification sent.")
    except Exception as exc:
        print(f"Failed to send email notification: {exc}")


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
    send_email(message)

    print("Notification(s) sent.")
else:
    print("No new months found.")
