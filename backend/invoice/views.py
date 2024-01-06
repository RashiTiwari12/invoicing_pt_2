from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .serializers import (
    UserSerializer,
    InvoiceSerializer,
    ItemSerializer,
    LoginSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from .data import *
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import *

# Create your views here.


class SignupView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created successfuly"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "login successful",
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                }
            )
        return Response(serializer.errors, status=401)


# class Invoiceview(APIView):
#     def get(self, request):
#         serializer = InvoiceSerializer(invoices_data, many=True).data
#         return Response(serializer)

#     def post(self, request):
#         data = request.data
#         data["invoice_id"] = len(invoices_data) + 1
#         serializer = InvoiceSerializer(data=data)
#         if serializer.is_valid():
#             invoices_data.append(serializer.data)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class SpecificInvoice(APIView):
#     def get(self, request, id):
#         for val in invoices_data:
#             if val["invoice_id"] == id:
#                 serializer = InvoiceSerializer(val).data
#                 return Response(serializer)
#         return Response({"message": "Invoice is not found"}, status=404)


class AddItemview(APIView):
    def post(self, request, invoice_id):
        for val in invoices_data:
            if val["invoice_id"] == invoice_id:
                data = request.data
                serializer = ItemSerializer(data=data)
                if serializer.is_valid():
                    val["items"].append(serializer.data)
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
        return Response({"message": "Invoice not found"}, status=404)


class InvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Invoice added"}, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        invoices = Invoices.objects.filter(user=request.user.id)
        serializer = InvoiceSerializer(invoices, many=True).data
        return Response(serializer)


class SpecificInvoice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        invoices = Invoices.objects.get(invoice_id=id, user=request.user.id)
        serializer = InvoiceSerializer(invoices).data
        return Response(serializer)


class AddItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invoice_id):
        invoice = Invoices.objects.get(pk=invoice_id)
        data = request.data
        print(data)
        data["invoice"] = invoice.invoice_id
        serializer = ItemSerializer(data=data)
        print(data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
