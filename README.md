# Co-WIN-Slot-Tracker

Co-win slot tracker is app that sends you a mail as soon as covid vaccination slot is available in your area.

---
## Usage

1. Download the file app.py
2. Change Pincode and date
```
pincode = 'xxxxxx'
date = '09-05-2021' # date for which appointment is required
```
3. Add sender email address and app password at this section of the code

```
user = 'sender@gmail.com'
app_password = 'jcxajkygiqnukudg' # a token for gmail
```
4. Run it with python app.py in cmd

> In order to get emails, you need to make configuration changes in your gmail account.
> Follow the instructions at https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317 to make those configurations.


