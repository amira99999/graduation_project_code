from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run_code/', views.run_code, name='run_code'),
    path('get_code_suggestion/', views.get_code_suggestion, name='get_code_suggestion'),
]
