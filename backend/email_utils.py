from email.message import EmailMessage
import smtplib
import os


def send_verification_email(to_email: str, code: str) -> bool:
    """Send a simple verification email containing the code. Returns True on success.
    If SMTP environment is not configured, returns False.
    """
    host = os.getenv("SMTP_HOST")
    if not host:
        return False
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS")

    msg = EmailMessage()
    sender = user if user else f"no-reply@{os.getenv('SMTP_HOST', 'local')}"
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = "Kode Verifikasi JKN Pintar"
    msg.set_content(f"Kode verifikasi Anda untuk JKN Pintar adalah: {code}\n\nJika Anda tidak meminta kode ini, abaikan email ini.")

    try:
        s = smtplib.SMTP(host, port, timeout=10)
        s.starttls()
        if user and pwd:
            s.login(user, pwd)
        s.send_message(msg)
        s.quit()
        return True
    except Exception:
        return False
