from django.urls import path
from . import views

urlpatterns = [
    path('', views.techlog_tools, name='techlogtools'),
]
