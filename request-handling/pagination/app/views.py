from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
import urllib
from app.settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    page = int(request.GET.get('page', 1))
    bus_stations_list = []
    with open(BUS_STATION_CSV, encoding='cp1251') as csvfile:
        stations_list = list(csv.DictReader(csvfile))
        for i in range((page - 1)*10, page*10 - 1):
            station_dict = {}
            station_dict['Name'] = stations_list[i]['Name']
            station_dict['Street'] = stations_list[i]['Street']
            station_dict['District'] = stations_list[i]['District']
            bus_stations_list.append(station_dict)
    next_page_url = reverse('bus_stations') + '?' + urllib.parse.urlencode({'page': page + 1})
    if page > 1:
        args = {'page': page - 1}
        prev_page_url = reverse('bus_stations') + '?' + urllib.parse.urlencode(args)
    else: 
        prev_page_url = None
    return render_to_response('index.html', context={
    	'bus_stations': bus_stations_list, 
    	'current_page': page,
    	'prev_page_url': prev_page_url,
    	'next_page_url': next_page_url
    	})