from django.shortcuts import render, redirect, get_object_or_404
from .models import TelogSpparts, Repairs
from techlog_tools.forms import RepairsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Функция страницы запчастей
@login_required
def telog_spparts(request):
    tspparts = TelogSpparts.objects.order_by('-date')  # all()
    return render(request, 'telog_spparts/tspparts.html', {
        "tspparts": tspparts
    })


# Функция детализации запчастей
@login_required
def sppart_details(request, telog_spparts_id):
    sppart = get_object_or_404(TelogSpparts, pk=telog_spparts_id)
    return render(request, 'telog_spparts/sppart_details.html', {'sppart': sppart})


#  Функция текущих/новых авторемонтов (ремонтов)
@login_required
def current_new_repairs(request):
    # __isnull - постфикс для поля завершения 'ready' ремонтов
    repairs = Repairs.objects.filter(user_performer=request.user, ready__isnull=True)
    if request.method == 'GET':
        return render(request, 'telog_spparts/repairs.html', {'repairs': repairs, 'form_rep': RepairsForm()})
    else:
        try:
            form = RepairsForm(request.POST)
            # создаём новую переменную из своей формы (forms.py)
            new_repairs = form.save(commit=False)  # commit=False - не сохраняя в БД
            # Присвоение значения текущего пользователя.
            new_repairs.user_performer = request.user  # Важно!!! - именно user, а не user_performer
            new_repairs.save()
            return redirect('currentnewrepairs')
        except ValueError:
            context = {'repairs': repairs, 'form_rep': RepairsForm(),
                       'error': 'Переданы неверные данные. Попробуйте повторно.'}
            return render(request, 'telog_spparts/repairs.html',
                          context)


# Функция текущих ремонтов (объеденена -->)
# (--> с предыдущей, незадействована)
# def current_repairs(request):
#     # __isnull - постфикс для поля завершения 'ready' ремонтов
#     repairs = Repairs.objects.filter(user_performer=request.user, ready__isnull=True)
#     return render(request, 'telog_spparts/repairs.html', {'repairs': repairs, 'form_rep': RepairsForm()})


# Функционал просмотра, редактирования и сохранения ремонта
@login_required
def view_repair(request, repair_pk):
    repair = get_object_or_404(Repairs, pk=repair_pk)
    if request.method == "GET":
        repform = RepairsForm(instance=repair)
        return render(request, 'telog_spparts/viewrepair.html', {'repair': repair, 'repform': repform})
    else:
        try:
            repform = RepairsForm(request.POST, instance=repair)
            repform.save()
            return redirect('currentnewrepairs')
        except ValueError:
            return render(request, 'telog_spparts/viewrepair.html',
                          {'repair': repair, 'repform': repform, 'error': "Неверные данные"})


# Завершение ремонтов
@login_required
def finished_repair(request, repair_pk):
    repair = get_object_or_404(Repairs, pk=repair_pk, user_performer=request.user)
    if request.method == "POST":
        repair.ready = timezone.now()
        repair.save()
        return redirect('currentnewrepairs')


# Удаление ремонта из БД
@login_required
def delete_repair(request, repair_pk):
    repair = get_object_or_404(Repairs, pk=repair_pk, user_performer=request.user)
    if request.method == "POST":
        repair.delete()
        return redirect('currentnewrepairs')


# Функция отображения страницы завершённых авторемонтов
@login_required
def completed_repairs(request):
    repairs = Repairs.objects.filter(user_performer=request.user, ready__isnull=False).order_by('-ready')
    return render(request, 'telog_spparts/completed_reps.html', {'repairs': repairs})
