from django.shortcuts import render, get_object_or_404
from .models import TelogSpparts


# Функция страницы инструментов
def telog_spparts(request):
    tspparts = TelogSpparts.objects.order_by('-date')  # all()
    return render(request, 'telog_spparts/tspparts.html', {
        "tspparts": tspparts
    })


def sppart_details(request, telog_spparts_id):
    sppart = get_object_or_404(TelogSpparts, pk=telog_spparts_id)
    return render(request, 'telog_spparts/sppart_details.html', {'sppart': sppart})
