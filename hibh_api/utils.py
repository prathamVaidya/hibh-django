from hibh.settings import IPGEOLOCATION_API_KEY, FRONTEND_URL, ALERT_EMAIL_TEMPLATE, BACKEND_URL, VERIFICATION_EMAIL_TEMPLATE
import uuid
import requests
from django.core.mail import send_mail
from django.template import Template, Context
from django.utils.html import format_html

    
def createRandomUUID():
    return str(uuid.uuid4())

# Function to fetch location data using the ipinfo.io API
def get_location_data(ip):
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={IPGEOLOCATION_API_KEY}&ip={ip}"
    response = requests.get(url)
    data = response.json()
    return data

def send_verification_email(tracker):
        # send alert email
        subject = 'Verify your Email to Enable Tracker ' + tracker['name'] 
        html_template = VERIFICATION_EMAIL_TEMPLATE

        template = Template(html_template)

        # Prepare the context data with the actual values
        context = Context({
            'name': tracker["name"],
            'email_token': tracker["email_token"],
            'backend_url': BACKEND_URL
        })

        html_message = format_html(template.render(context))

        recipient_list = [tracker['email']]
        send_mail(subject, None, None, recipient_list, html_message=html_message)

def send_alert_email(tracker, alert):
        # send alert email
        subject = 'Alert: Your Tracker ' + tracker.name + " just Triggered!" 
        html_template = ALERT_EMAIL_TEMPLATE

        template = Template(html_template)

        # Prepare the context data with the actual values
        context = Context({
            'tracker': tracker,
            'alert': alert,
            'frontend_url': FRONTEND_URL
        })

        html_message = format_html(template.render(context))

        recipient_list = [tracker.email]
        send_mail(subject, None, None, recipient_list, html_message=html_message)

def createHTMLTrackerFile(tracker):
    html = """
    test
    """
    return html