import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_alert(recipient, subject, message):
    """Send an email alert when a threat is detected."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        # Gmail SMTP server (SSL)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print("✅ Email alert sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")
