from django.urls import path

from app.views import file_list, file_content


urlpatterns = [
	path('', file_list, name='file_list'),
	path('<str:date>/', file_list, name='file_list'),
	path('files/<str:name>/', file_content, name='file_content'),
]
