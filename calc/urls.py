from django.urls import path
from . import views


app_name = "calc"
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('results', views.result, name='result'),
    path('results/xls', views.to_xlsx, name='xls'),
    path('results/pdf', views.bar_chart, name='pdf'),
]
