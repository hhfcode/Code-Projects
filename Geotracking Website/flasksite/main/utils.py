from flask import url_for
from flask_mail import Message
from flasksite import mail


def send_SoS_message(email):
    msg = Message('SoS Message - Danger Danger',
                  sender='noreply@demo.com',
                  recipients=[email.email])
    msg.body = f'''Warning: This is an Autonomous SOS Signal
{url_for('map.displaymap', _external=True)}
A Bike has left the Pass Zone - Perhaps This is a controlled test, and this email can be ignored.
If this is NOT a test - Please inform the proper management. Call authorities (Phonenumber: 112 - In Denmark )
Or Contract the Military
https://www2.forsvaret.dk/kontakt/Pages/default.aspx
'''
    mail.send(msg)