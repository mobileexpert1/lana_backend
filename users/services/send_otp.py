from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_otp_to_mail(username, otp, user_email):
    html_message = render_to_string('mail/otp.html', {
        'username': username,
        'otp': otp,
    })

    plain_message = strip_tags(html_message)
    subject = 'OTP for Verification'

    send_mail(
        subject,
        plain_message,
        'cspc186@gmail.com',
        [user_email],
        html_message=html_message
    )
