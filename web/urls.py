from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('newsearch', views.new_search, name = 'new_search'),
]
