from datetime import datetime
from twilio.rest import Client
import os
import sys
import django
from dotenv import load_dotenv

# ----------------------------
# Load environment variables
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Get Twilio credentials from .env
account_sid = os.getenv("ACCOUNT_SID").strip()
auth_token = os.getenv("AUTH_TOKEN").strip()

# ----------------------------
# Set up Django environment
# ----------------------------
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websracping_backend.settings")
django.setup()

from webscrapper.db_hits import get_data

# ----------------------------
# Twilio Client
# ----------------------------
client = Client(account_sid, auth_token)



def send_message():
    print("⏰ Cron Triggered:", datetime.now())
    try:
        company_data = get_data()
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+919494667649',
            body=company_data,
        )
        print("✅ Message sent:", message.sid)
    except Exception as e:
        print("❌ Error:", str(e))

if __name__ == "__main__":
    send_message()
