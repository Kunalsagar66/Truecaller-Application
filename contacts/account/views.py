from django.shortcuts import render
import logging
import uuid

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *

# Create your views here.


class RegisterUser(APIView):
    """
    A class to register the user to the application
    """

    def post(self, request):
        try:
            if request.data:
                logging.info("****************************** Register View ******************************")
                user_details = RegisterUserSerializer(data=request.data)
                if user_details.is_valid(raise_exception = True):
                    username = user_details.validated_data['username']
                    name = user_details.validated_data['name']
                    phone_number = user_details.validated_data['phone_number']
                    password = user_details.validated_data['password']
                    email = user_details.validated_data.get('email', '')

                    existing_username = Account.objects.filter(username=username)
                    if(existing_username):
                        return Response(data= {"message":"Username already exist"}, status= status.HTTP_400_BAD_REQUEST)
                    existing_phone = Account.objects.filter(phone_number=phone_number)
                    if(existing_phone):
                        return Response(data= {"message":"User already exist with given phone number"}, status= status.HTTP_400_BAD_REQUEST)
                    
                    user = Account.objects.create_user(name=name, username=username, phone_number=phone_number, password=password)

                    if email:
                        user.email = email 

                    user.save()

                    return Response(data=user_details.data, status = status.HTTP_201_CREATED)
                else:
                    return Response(data= {"message":"User details is not valid"}, status= status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data= {"message":"User details not provided"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logging.error(f'Error in registering user : {str(error)}')
            return Response(data= {"message":str(error)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUser(APIView):
    """
    API to logging in the user
    """
    def post(self,request):
        try:
            if request.data:
                logging.info("****************************** Login View ******************************")
                user_details = LoginUserSerializer(data=request.data)
                if user_details.is_valid(raise_exception = True):
                    username = user_details.validated_data['username']
                    password = user_details.validated_data['password']

                    user = authenticate(username=username,password = password)
                    token, _ =Token.objects.get_or_create(user = user)
                    res = {"User":user,"Token":token.key}
                    return Response(data=res,status=status.HTTP_200_OK)
                else:
                    return Response(data= {"message":"User details is not valid"}, status= status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data= {"message":"Username/password not provided"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logging.error(f'Error in logging user : {str(error)}')
            return Response(data= {"message":str(error)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserToken(APIView):
    """
    API to generate and return a token for the user
    """

    def post(self, request):
        try:
            if request.data:
                logging.info("****************************** Get User Token View ******************************")
                user_details = LoginUserSerializer(data=request.data)
                if user_details.is_valid(raise_exception = True):
                    username = user_details.validated_data['username']
                    password = user_details.validated_data['password']
                    user = Account.objects.get(username=username)

                    token = str(uuid.uuid4())

                    user_token, created = UserToken.objects.update_or_create(
                        user=user,
                        defaults={'token': token, 'is_active': True}
                    )

                    serializer = UserTokenSerializer(user_token)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(data= {"message":"User details is not valid"}, status= status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data= {"message":"Username/password not provided"}, status= status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserToken(APIView):
    """
    API to verify if the token is active for the user
    """

    def get(self, request):
        try:
            logging.info("****************************** Verify User Token View ******************************")
            token = request.headers.get('Token')

            user_token = UserToken.objects.filter(token=token, is_active=True).first()

            if user_token:
                return Response({"message": "Token is valid","code":0}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid or inactive token","code":101}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error:
            return Response({"message": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)