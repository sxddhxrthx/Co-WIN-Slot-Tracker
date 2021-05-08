import requests
import json
import time
import yagmail
from datetime import datetime

pincode = '470113'
date = '09-05-2021'

def get_request_params():

    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}"

    payload={}
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    return url, payload, headers

def get_sessions():

    url, payload, headers = get_request_params()

    response = requests.request("GET", url, headers=headers, data=payload)

    schedule_data = json.loads(response.text)

    sessions = schedule_data['sessions']

    current_time = datetime.now()
    if sessions:
        for session in sessions:
            print(f"{current_time} -- ({session['min_age_limit']}+) {session['address']}: {session['available_capacity']}")
            if int(session['min_age_limit']) == 18:
                send_mail()
    else:
        print(f"{current_time} -- Session Not Available")

def compose_mail():

    subject = 'VACCINE Available for 18+ in your area'
    body = 'Covid Vaccine available in your area for age 18-44'

    return subject, body


def send_mail():

    user = 'user@gmail.com'
    app_password = '<your app password>' # a token for gmail
    to = 'recipient@gmail.com'

    subject = 'VACCINE Available for 18+ in your area'
    subject, content = compose_mail()

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')

while True:
    get_sessions()
    time.sleep(4)
