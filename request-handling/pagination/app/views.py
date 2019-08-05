from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from urllib.parse import urlencode
from app.settings import BUS_STATION_CSV
from django.core.paginator import Paginator

def index(request):
    return redirect(reverse(bus_stations))

def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    bus_stations_list = []
    with open(BUS_STATION_CSV, encoding='cp1251') as csvfile:
        file_content = list(csv.DictReader(csvfile))
        paginator = Paginator(file_content, 10)
        rows_count = paginator.count
        total_pages = paginator.num_pages
        first_row = (page_number - 1)*10
        if page_number != total_pages:
            last_row = page_number*10 - 1
        else:
            last_row = rows_count
        for i in range(first_row, last_row):
            station_dict = {}
            station_dict['Name'] = file_content[i]['Name']
            station_dict['Street'] = file_content[i]['Street']
            station_dict['District'] = file_content[i]['District']
            bus_stations_list.append(station_dict)             
        page = paginator.page(page_number)
        if page.has_next():
            next_page_url = reverse('bus_stations') + '?' + urlencode({'page': page_number + 1})
        else:
            next_page_url = None
        if page.has_previous():
            prev_page_url = reverse('bus_stations') + '?' + urlencode({'page': page_number - 1})
        else:
            prev_page_url = None
    return render_to_response('index.html', context={
        'bus_stations': bus_stations_list, 
        'current_page': page_number,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url
        })