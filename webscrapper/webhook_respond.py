from IPython.core.completerlib import import_re
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.rest import Client
from webscrapper.db_hits import get_data
from webscrapper.models import RecentCount
from webscrapper.ai_scrapping_details import *
from dotenv import load_dotenv
load_dotenv()
import os
# Twilio Credentials

twilio_number = "whatsapp:+14155238886"
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
client = Client(account_sid, auth_token)

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        body = request.POST.get('Body', '').strip().lower()
        from_number = request.POST.get('From')  # This is the user's WhatsApp number

        if "deep" in body and "dive" in body:
            recent_entry = RecentCount.objects.last()
            if recent_entry:
                company_details = recent_entry.recent_company_id
                ai_text = get_more_company_details(company_details)


                client.messages.create(
                    from_=twilio_number,
                    to=from_number,
                    body=ai_text
                )
                return HttpResponse("Deep dive sent via Twilio", status=200)
            else:
                client.messages.create(
                    from_=twilio_number,
                    to=from_number,
                    body="No company found to deep dive."
                )
                return HttpResponse("No company found", status=200)

        elif body == "next":
            from twilio.twiml.messaging_response import MessagingResponse
            response = MessagingResponse()
            reply_text = get_data()
            response.message(reply_text)
            return HttpResponse(str(response), content_type='text/xml')

        else:
            from twilio.twiml.messaging_response import MessagingResponse
            response = MessagingResponse()
            response.message("Reply 'Next' for next company or 'Deep Dive' for details.")
            return HttpResponse(str(response), content_type='text/xml')

    return HttpResponse("Only POST allowed", status=405)
