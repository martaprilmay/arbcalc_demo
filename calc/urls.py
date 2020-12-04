from django.urls import path
from . import views


app_name = "calc"
urlpatterns = [
    path('', views.home, name='home'),
    path('ru', views.home_ru, name='home-ru'),
    path('about', views.about, name='about'),
    path('ru/about', views.about_ru, name='about-ru'),
    path('results', views.result, name='result'),
    path('ru/results', views.result_ru, name='result-ru'),
    path('results/xls', views.to_xlsx, name='xls'),
    path('ru/results/xls', views.to_xlsx_ru, name='xls-ru'),
    path('results/pdf', views.bar_chart, name='pdf'),
    path('ru/results/pdf', views.bar_chart_ru, name='pdf-ru'),
]
