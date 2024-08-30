from django.urls import path
from .views import *
urlpatterns = [
    path('register', RegisterUser.as_view(),name='register'),
    path('login', LoginUser.as_view(),name='login'),
    path('get-user-token', GetUserToken.as_view(),name='get_user_token'),
    path('verify-token', VerifyUserToken.as_view(),name='verify_token'),

]