from django.urls import path
from . import views

urlpatterns = [
    path('', views.telog_spparts, name='telogspparts'),
    path('<int:telog_spparts_id>', views.sppart_details, name='sppart_details'),
    # path('new_repairs/', views.create_repairs, name='createrepairs'),
    path('current_new_repairs/', views.current_new_repairs, name='currentnewrepairs'),
    path('current_new_repairs/<int:repair_pk>', views.view_repair, name='viewrepair'),
    path('current_new_repairs/<int:repair_pk>/finished/', views.finished_repair, name='finished_repair'),
    path('current_new_repairs/<int:repair_pk>/delete/', views.delete_repair, name='delete_repair'),
    path('current_new_repairs/completed/', views.completed_repairs, name='completed_reps'),
]
# в base.html используется, например name='currentnewrepairs'
# в теге  <a href="{% url 'currentnewrepairs' %}"> %}", как
# ссылка на модуль создания / проведения новых ремонтов
