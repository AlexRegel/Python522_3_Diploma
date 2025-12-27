from django.urls import path
from . import views

urlpatterns = [
    path('', views.telog_spparts, name='telogspparts'),
    path('<int:telog_spparts_id>', views.sppart_details, name='sppart_details'),
    path('repairs/', views.create_repairs, name='createautorepairs'),
]
# в base.html используется, например name='createautorepairs'
# в теге  <a href="{% url 'createautorepairs' %}"> %}", как
# ссылка на модуль создания / проведения новых ремонтов
