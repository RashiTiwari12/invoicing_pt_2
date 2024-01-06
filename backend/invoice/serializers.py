from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoices
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            # name=validated_data["name"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "password")

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError("username or password does not match")
