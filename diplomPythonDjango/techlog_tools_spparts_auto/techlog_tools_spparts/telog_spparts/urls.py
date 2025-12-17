from django.urls import path
from . import views

urlpatterns = [
    path('', views.telog_spparts, name='telogspparts'),
    path('<int:telog_spparts_id>', views.sppart_details, name='sppart_details'),
]
