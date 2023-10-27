from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .settings import EMAIL_MESSAGE

import smtplib

import paypalrestsdk


class EmailSender:
    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.server, self.port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            return True
        except Exception as e:
            return False

    def send_payment_success(self, to_email):
        return self.send_email(
            to_email=to_email,
            subject="Payment Successful",
            body=EMAIL_MESSAGE
        )


class PayPalPaymentService:
    def create_payment(self, amount, confirmation_url, cancel_url):
        return paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal",
                },
                "transactions": [
                    {
                        "amount": {
                            "total": amount,
                            "currency": "USD",
                        },
                        "description": "Оплата за участие в мероприятии Netday",
                    }
                ],
                "redirect_urls": {
                    "return_url": confirmation_url,
                    "cancel_url": cancel_url
                },
            }
        )
