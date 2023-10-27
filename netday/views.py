from django.shortcuts import redirect
from paypalrestsdk import ResourceNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Registration
from .serializers import RegistrationSerializer
from .settings import *
import paypalrestsdk
from .services import EmailSender, PayPalPaymentService


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    http_method_names = ['get', 'post']

    payment_service = PayPalPaymentService()

    email_sender = EmailSender(
        server=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD
    )

    def get(self, request):
        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        try:
            payment = paypalrestsdk.Payment.find(payment_id)
        except ResourceNotFound:
            return redirect(FRONTEND_INDEX_PAGE_URL)

        if payment.execute({"payer_id": payer_id}) and payment.state in ["approved", "completed"]:
            registration = Registration.objects.get(payment_id=payment_id)
            registration.isPay = True
            registration.save()
            self.email_sender.send_payment_success(registration.email)
            return redirect(FRONTEND_INDEX_PAGE_URL)

        return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration = Registration(**serializer.validated_data)

        existing_registration = Registration.objects.filter(email=registration.email).first()

        if existing_registration and existing_registration.isPay:
            return Response({"message": "Email already registered"}, status=status.HTTP_409_CONFLICT)

        if existing_registration:
            existing_registration.delete()

        payment = self.payment_service.create_payment(
            amount=PAYMENT_AMOUNT,
            confirmation_url=PAYMENT_CONFIRMATION_URL,
            cancel_url=FRONTEND_INDEX_PAGE_URL
        )

        if not payment.create():
            return Response({"message": "Failed to create payment"}, status=status.HTTP_400_BAD_REQUEST)

        payment_url = None

        for link in payment.links:
            if link.method == 'REDIRECT':
                payment_url = link.href
                break

        registration.payment_id = payment.id
        registration.save()

        return Response({"redirect_url": payment_url}, status=status.HTTP_200_OK)
