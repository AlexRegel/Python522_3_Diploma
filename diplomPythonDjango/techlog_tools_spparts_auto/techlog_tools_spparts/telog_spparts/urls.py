from django.urls import path
from . import views

urlpatterns = [
    path('', views.telog_spparts, name='telogspparts'),
]
