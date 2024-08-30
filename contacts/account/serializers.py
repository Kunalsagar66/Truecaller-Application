from rest_framework import serializers
from .models import*
from contact.models import *

class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(required =True)
    name = serializers.CharField(required = True)
    phone_number = serializers.IntegerField(required = True)
    email = serializers.CharField(required =False, allow_blank=True)
    password = serializers.CharField(required =True)
    
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required =True)
    password = serializers.CharField(required =True)
    

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ['user', 'token', 'is_active']

class MarkSpamSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(required = True)

class SearchByNameSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)

class AccountResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'phone_number','email','is_spam']  

class ContactResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'is_spam']  