from django.shortcuts import render, redirect, reverse
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializers import EventdataSerializers
import pandas as pd
import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
from datetime import datetime, timedelta

load_dotenv()

def getdata(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        date = request.POST.get('date')


        file_path = '~/Documents/Event-management-system/mainapp/files/dataset.csv'
        df = pd.read_csv(file_path, delimiter=',')
        df = df.astype(str)
        check=0
        for i in range(len(df)):
            try:
                Eventdata.objects.create(
                    id=i,
                    event_name=df.values[i][0],
                    city_name=df.values[i][1],
                    date= datetime.strptime(df.values[i][2], '%Y-%m-%d').date(),
                    latitude=df.values[i][3],
                    longitude=df.values[i][4]
                )
            except IntegrityError:
                check=1

        if check == 1:
            print("the data of evnets already exists")

        return redirect(reverse('event:getevents')+f'?latitude={latitude}&longitude={longitude}&date={date}')
    return render(request, 'form.html')


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetEventsListAPIView(generics.ListAPIView):
    serializer_class = EventdataSerializers
    queryset = Eventdata.objects.all()
    pagination_class = CustomPagination

    def get_weather_distance(self, latitude1, longitude1, latitude2, longitude2, date, city_name):
        params_weather = {
            'code': os.getenv("weather_code"),
            'city': city_name,
            'date': date
        }
        encoded_params_weather = urlencode(params_weather)
        weather_base_url = "https://gg-backend-assignment.azurewebsites.net/api/Weather"
        full_weather_url = f'{weather_base_url}?{encoded_params_weather}'
        try:
            weather_response = requests.get(full_weather_url)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
            else:
                weather_data = {}
                print(f"Error: {weather_response.status_code} - {weather_response.reason}")
        except Exception as e:
            print(e)

        params_distance = {
            'code': os.getenv("distance_code"),
            'latitude1': latitude1,
            'longitude1': longitude1,
            'latitude2': latitude2,
            'longitude2': longitude2,
        }
        
        encoded_params_distance = urlencode(params_distance)
        distance_base_url = "https://gg-backend-assignment.azurewebsites.net/api/Distance"
        full_distance_url = f'{distance_base_url}?{encoded_params_distance}'
        distance_response = requests.get(full_distance_url)
        if distance_response.status_code == 200:
            distance_data = distance_response.json()
        else:
            distance_data = {}
            print(f"Error: {distance_response.status_code} - {distance_response.reason}")

        return {**weather_data, **distance_data}

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get('date')
        parse_date = datetime.strptime(date, '%Y-%m-%d').date()
        return (
            queryset.filter(date__gte=parse_date)
            .filter(date__lte=parse_date+timedelta(days=13)).order_by('date')
        )
    
    def generate_result(self, serialized_data, request_data):
        result_data = []
        for item in serialized_data:
            data = self.get_weather_distance(
                request_data.get('latitude'), request_data.get('longitude'),
                item['latitude'], item['longitude'],
                request_data.get('date'), item['city_name']
            )
            item.pop("latitude")
            item.pop("longitude")
            result_data.append({**item, **data})
        return result_data
    
    def list(self, request, *args, **kwargs):
        request_data = request.GET
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = serializer.data
            result_data = self.generate_result(paginated_data, request_data)
            return self.get_paginated_response(result_data)

        serializer = self.get_serializer(queryset, many=True)
        result_data = self.generate_result(serializer.data, request_data)
        return Response(result_data)

