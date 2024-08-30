from django.shortcuts import render
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from account.serializers import *

from account.decorator import token_required
# Create your views here.

class MarkSpam(APIView):
    """
    A class to mark phone number as spam
    """
    @token_required
    def post(self,request):
        try:
            if request.data:
                logging.info("****************************** Mark Spam View ******************************")
                user_details = MarkSpamSerializer(data=request.data)
                if user_details.is_valid(raise_exception = True):
                    phone_number = user_details.validated_data['phone_number']

                    token = request.headers.get('token')
                    user = UserToken.objects.filter(token=token).first().user

                    if(Spam.objects.filter(phone_number=phone_number)):
                        return Response(data={"message":"Phone number already marked as spam","phone_number":phone_number}, 
                                    status=status.HTTP_200_OK)

                    spam_user = Spam.objects.create(user=user,phone_number=phone_number)

                    registered_user = Account.objects.filter(phone_number=phone_number).update(is_spam=True)

                    global_contact_user = Contact.objects.filter(phone_number=phone_number).update(is_spam=True)

                    return Response(data={"message":"Phone number marked as spam","phone_number":phone_number}, 
                                    status=status.HTTP_200_OK)
                else:
                    return Response(data= {"message":"Phone number is not valid"}, status= status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data= {"message":"Phone number is not provided"}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logging.error(f'Error in marking phone number as spam : {str(error)}')
            return Response(data= {"message":str(error)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchByName(APIView):
    """
    A class to search in the contact list by name
    """
    @token_required
    def get(self,request):
        try:
            query_params = {'name': request.query_params.get('name', None)}
            if query_params:
                logging.info("****************************** Search By Name View ******************************")
                user_details = SearchByNameSerializer(data=query_params)
                if user_details.is_valid(raise_exception = True):
                    name = user_details.validated_data['name']

                    accounts_start_with = Account.objects.filter(name__istartswith=name)
                    contacts_start_with = Contact.objects.filter(name__istartswith=name)

                    accounts_contains = Account.objects.filter(name__icontains=name).exclude(name__istartswith=name)
                    contacts_contains = Contact.objects.filter(name__icontains=name).exclude(name__istartswith=name)

                    accounts = accounts_start_with | accounts_contains
                    contacts = contacts_start_with | contacts_contains

                    account_serializer = AccountResponseSerializer(accounts, many=True)
                    contact_serializer = ContactResponseSerializer(contacts, many=True)

                    token = request.headers.get('token')
                    searcher_number = UserToken.objects.filter(token=token).first().user.phone_number
                    accounts_list = list(account_serializer.data)
                    for account in accounts_list:
                        account_instance = Account.objects.get(phone_number=account['phone_number'])
                        searcher_contact_exists = Contact.objects.filter(user=account_instance, phone_number=searcher_number).exists()
                        if not searcher_contact_exists:
                            account.pop('email', None)

                    final_list = accounts_list + contact_serializer.data

                    response_data = {
                        'result': final_list,
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(data= {"message":"Given name is not valid query param"}, status= status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data= {"message":"name is not provided in query params"}, status= status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            logging.error(f'Error in searching user by name : {str(error)}')
            return Response(data= {"message":str(error)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchByNumber(APIView):
    """
    A class to search in the contact list by name
    """
    @token_required
    def get(self,request):
        try:
            query_params = {'phone_number': request.query_params.get('phone_number', None)}
            if query_params:
                logging.info("****************************** Search By Number View ******************************")
                user_details = MarkSpamSerializer(data=query_params)
                if user_details.is_valid(raise_exception = True):
                    phone_number = user_details.validated_data['phone_number']

                    accounts_with_number = Account.objects.filter(phone_number=phone_number)
                    if accounts_with_number:
                        token = request.headers.get('token')
                        searcher_number = UserToken.objects.filter(token=token).first().user.phone_number
                        searcher_contact_exists = Contact.objects.filter(user__in=accounts_with_number, phone_number=searcher_number).exists()
                        account_serializer = AccountResponseSerializer(accounts_with_number, many=True)
                        res = list(account_serializer.data)
                        if not searcher_contact_exists:
                            for account in res:
                                account.pop('email', None)

                        response_data = {
                            'result': res,
                        }

                        return Response(response_data, status=status.HTTP_200_OK)
                    
                    contacts_with_number = Contact.objects.filter(phone_number=phone_number)
                    contact_serializer = ContactResponseSerializer(contacts_with_number, many=True)

                    response_data = {
                        'result': contact_serializer.data,
                    }

                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response(data= {"message":"Given phone_number is not valid query param"}, status= status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data= {"message":"phone_number is not provided in query params"}, status= status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            logging.error(f'Error in searching user by phone_number : {str(error)}')
            return Response(data= {"message":str(error)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)