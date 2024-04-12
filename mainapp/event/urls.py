from django.urls import path
from django import views
from . import views
from .views import GetEventsListAPIView

app_name = "event"
urlpatterns = [
    path('', views.getdata, name='getdata'),
    path('getevents/', GetEventsListAPIView.as_view(), name='getevents')
]
