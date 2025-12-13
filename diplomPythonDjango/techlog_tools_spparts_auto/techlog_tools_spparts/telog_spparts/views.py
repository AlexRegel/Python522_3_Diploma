from django.shortcuts import render
from .models import TelogSpparts


# Функция страницы инструментов
def telog_spparts(request):
    tspparts = TelogSpparts.objects.all()
    return render(request, 'telog_spparts/tspparts.html', {
        "tspparts": tspparts
    })
