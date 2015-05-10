# -*- coding: utf-8 -*-

from twilio.rest import TwilioRestClient

from mailhook.config.config import TWILIO_NUMBER, TWILIO_TOKEN, TWILIO_SID


def get_twilio():
    return TwilioRestClient(TWILIO_SID, TWILIO_TOKEN)


def send_picture(recipient, media_url):
    twclient = get_twilio()
    message = twclient.messages.create(
        from_=TWILIO_NUMBER,
        to=recipient,
        media_url=media_url,
    )
    return message
