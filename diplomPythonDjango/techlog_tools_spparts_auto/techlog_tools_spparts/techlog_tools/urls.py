from django.urls import path
from . import views

urlpatterns = [
    path('', views.techlog_tools, name='techlogtools'),
    path('<int:techlog_tools_id>', views.tool_details, name='tool_details'),
]
