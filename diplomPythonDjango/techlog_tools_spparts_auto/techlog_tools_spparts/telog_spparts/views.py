from django.shortcuts import render, get_object_or_404
from .models import TelogSpparts, Repairs
from techlog_tools.forms import RepairsForm


# Функция страницы запчастей
def telog_spparts(request):
    tspparts = TelogSpparts.objects.order_by('-date')  # all()
    return render(request, 'telog_spparts/tspparts.html', {
        "tspparts": tspparts
    })


# Функция детализации запчастей
def sppart_details(request, telog_spparts_id):
    sppart = get_object_or_404(TelogSpparts, pk=telog_spparts_id)
    return render(request, 'telog_spparts/sppart_details.html', {'sppart': sppart})


#  Функция создания/обработки ремонтов
def create_repairs(request):
    # repairs = Repairs.objects.all()
    if request.method == 'GET':
        return render(request, 'telog_spparts/repairs.html', {'form': RepairsForm()})
    # {'repairs': repairs}
