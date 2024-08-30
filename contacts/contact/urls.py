from django.urls import path
from .views import *
urlpatterns = [
    path('mark-spam', MarkSpam.as_view(),name='mark_spam'),
    path('search-name', SearchByName.as_view(),name='search_by_name'),
    path('search-number', SearchByNumber.as_view(),name='search_by_number'),

]