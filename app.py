import requests
import json
import time
import yagmail
import sys
from datetime import datetime
from win10toast import ToastNotifier

date = sys.argv[1]
age_agroup = sys.argv[2]

def get_recipients():

    recipients = {
        "123456": ["recipient1@email.com", "recipient2@email.com"],
        "100100": ["recipient3@email.com"],
        "101010": ["recipient4@email.com", "recipient5@email.com",  "recipient6@email.com"]
    }

    return recipients

def get_request_params(pincode, date):

    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}"
    payload={}
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    return url, payload, headers

def get_session_data(pincode, date):

    url, payload, headers = get_request_params(pincode, date)
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        schedule_data = json.loads(response.text)
        sessions = schedule_data['sessions']
        return sessions
    except Exception as e:
        print(f"{current_time} - {pincode} - No Response from API - Error: {e}")
        return []
    

def check_vaccine_availability(sessions, pincode):

    current_time = datetime.now()
    if sessions:
        for session in sessions:
            print(f"{current_time} - {session['pincode']} - ({session['min_age_limit']}+) {session['address']}: {session['available_capacity']}")
            if int(session['min_age_limit']) == age_agroup:
                return True
    else:
        print(f"{current_time} - {pincode} - Session Not Available")
        return False


def compose_mail(pincode, center_details):

    subject = f'VACCINATION SLOT AVAILABLE at PINCODE {pincode}'
    body = '''
    Covid Vaccine available in your area for age group 45+.
    Vaccine is available at following centers:
    '''

    for count, center in enumerate(center_details):
        body += f'''
        {count+1}. {center}
        '''

    body += '''
    Kindly use navigation tools to locate these addresses.

    Regards,
    Co-WIN BOT
    created by siddhartha chowdhury
    '''

    return subject, body


def send_mail(recipient, subject, content):

    user = '<sender_email_id>'
    app_password = '<sender_app_password>'

    to = recipient

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')


def get_vaccine_centers(session_data):

    vaccine_centers = []

    for location in session_data:
        address = location['address']
        vaccine_centers.append(address)

    return vaccine_centers


def run():

    recipients = get_recipients()

    for receipient in recipients.items():

        pincode = receipient[0]
        email_addresses = receipient[1]
        session_data = get_session_data(pincode, date)
        available = check_vaccine_availability(session_data, pincode)

        if available:
            vaccine_centers = get_vaccine_centers(session_data)
            subject, mail_body = compose_mail(pincode, vaccine_centers)
            for email_address in email_addresses:
                send_mail(email_address, subject, mail_body)


    # quit(1)

while True:
    run()
    time.sleep(5)
