from django.shortcuts import redirect
from paypalrestsdk import ResourceNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Registration
from .forms import RegistrationForm
from .settings import EMAIL_MESSAGE, FRONTEND_URL, PAYMENT_CONFIRMATION_URL
import paypalrestsdk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class RegistrationView(APIView):

    def get(self, request):
        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        try:
            payment = paypalrestsdk.Payment.find(payment_id)
        except ResourceNotFound:
            return redirect(FRONTEND_URL)

        if payment.execute({"payer_id": payer_id}):
            if payment.state == "approved" or payment.state == "completed":
                registration = Registration.objects.get(payment_id=payment_id)
                registration.isPay = True
                send_payment_success_email(registration.email)
                registration.save()
            return redirect(FRONTEND_URL)

        return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        form_data = request.data
        print(request.data)
        payment_amount = 0.1
        form = RegistrationForm(form_data)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            registration = Registration.objects.filter(email=email, isPay=True).first()
            if registration:
                return Response({"message": "Email already registered"}, status=status.HTTP_409_CONFLICT)
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal",
                },
                "transactions": [
                    {
                        "amount": {
                            "total": str(payment_amount),
                            "currency": "USD",
                        },
                        "description": "Оплата за участие в мероприятии Netday",
                    }
                ],
                "redirect_urls": {
                    "return_url": PAYMENT_CONFIRMATION_URL,
                    "cancel_url": FRONTEND_URL
                },
            })
            if payment.create():
                for link in payment.links:
                    if link.method == "REDIRECT":
                        registration = Registration(
                            name=form.cleaned_data.get("name"),
                            surname=form.cleaned_data.get("surname"),
                            email=email,
                            phone_number=form.cleaned_data.get("phone_number"),
                            country=form.cleaned_data.get("country"),
                            university=form.cleaned_data.get("university"),
                            major=form.cleaned_data.get("major"),
                            course=form.cleaned_data.get("course"),
                            isPay=False
                        )
                        registration.payment_id = payment.id
                        registration.save()
                        return Response({"redirect_url": link.href}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to create payment"}, status=status.HTTP_400_BAD_REQUEST)


def send_payment_fail_email(to_email):
    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = 587
    smtp_username = os.getenv("EMAIL_HOST_USER")
    smtp_password = os.getenv("EMAIL_HOST_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg["Subject"] = "Payment Successful"

    body = os.getenv("FAILED_PAYMENT_MESSAGE")
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_email, text)
        server.quit()
        return Response({"message": "Message succuesfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Message failed"}, status=status.HTTP_400_BAD_REQUEST)


def send_payment_success_email(to_email):
    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = 587
    smtp_username = os.getenv("EMAIL_HOST_USER")
    smtp_password = os.getenv("EMAIL_HOST_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg["Subject"] = "Payment Successful"

    body = EMAIL_MESSAGE
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_email, text)
        server.quit()
        return Response({"message": "Message succuesfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Message failed"}, status=status.HTTP_400_BAD_REQUEST)
