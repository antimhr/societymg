from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from society import settings


@shared_task
def send_email_task(email, user_otp):
    mess = f"Hello {email}, \n Your OTP is {user_otp} \n Thank You"
    send_mail(
        "Welcome",
        mess,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    print("email sent")

