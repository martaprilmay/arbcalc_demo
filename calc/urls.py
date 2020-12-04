from django.urls import path
from . import views


app_name = "calc"
urlpatterns = [
    path('', views.home, name='home'),
    path('ru', views.home_ru, name='home-ru'),
    path('about', views.about, name='about'),
    path('results', views.result, name='result'),
    path('results/ru', views.result_ru, name='result-ru'),
    path('results/xls', views.to_xlsx, name='xls'),
    path('results/xlsru', views.to_xlsx_ru, name='xls-ru'),
    path('results/pdf', views.bar_chart, name='pdf'),
    path('results/pdfru', views.bar_chart_ru, name='pdf-ru'),
]
