# VHS Bamberg Monitor

Automatically checks the VHS Bamberg page daily for these month/date values:
- 06.2026
- 07.2026
- 08.2026
- 09.2026
- 10.2026
- 11.2026

If found:
- sends Telegram notification

## Setup

Add these GitHub repository secrets:

- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- EMAIL_SMTP_HOST
- EMAIL_SMTP_PORT
- EMAIL_SMTP_USER
- EMAIL_SMTP_PASSWORD
- EMAIL_FROM
- EMAIL_TO

`EMAIL_TO` can be a single address or a comma-separated list of recipients.

### Gmail example

For Gmail, use these values:

- `EMAIL_SMTP_HOST`: `smtp.gmail.com`
- `EMAIL_SMTP_PORT`: `587`
- `EMAIL_SMTP_USER`: your Gmail address
- `EMAIL_SMTP_PASSWORD`: an app password from Google
- `EMAIL_FROM`: your Gmail address
- `EMAIL_TO`: recipient@example.com

> Note: Gmail typically requires an app password for SMTP access when using third-party automation.
