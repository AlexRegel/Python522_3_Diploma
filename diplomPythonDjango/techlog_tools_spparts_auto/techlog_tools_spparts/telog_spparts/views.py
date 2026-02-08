from django.shortcuts import render, redirect, get_object_or_404
from .models import TelogSpparts, Repairs
from techlog_tools.forms import RepairsForm, SpparstAddedForm, CalcForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.forms import formset_factory


# Функция страницы запчастей
@login_required
def telog_spparts(request):
    tspparts = TelogSpparts.objects.order_by('-date')  # all()
    return render(request, 'telog_spparts/tspparts.html', {
        "tspparts": tspparts,
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
            context = {
                'repairs': repairs,
                'form_rep': RepairsForm(),
                'error': 'Переданы неверные данные. Попробуйте повторно.',
            }
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
        context = {'repair': repair, 'repform': repform}
        return render(request, 'telog_spparts/viewrepair.html', context)
    else:  # request.method == "POST"
        try:
            repform = RepairsForm(request.POST, instance=repair)
            repform.save()
            return redirect('currentnewrepairs')
        except ValueError:
            context = {'repair': repair, 'repform': repform, 'error': "Неверные данные"}
            return render(request, 'telog_spparts/viewrepair.html',
                          context)


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


# Функционал по добавлению запчастей со стороны сайта
@login_required
def added_spparts(request):
    try:
        if request.method == "POST":
            # ОБЯЗАТЕЛЬНО добавляем request.FILES для обработки изображений
            form = SpparstAddedForm(request.POST, request.FILES)
            if form.is_valid():
                new_form_add = form.save(commit=False)
                new_form_add.user_who_added = request.user
                new_form_add.save()
                return redirect('addedspparts')
            else:
                # Если форма невалидна,
                # проходим вниз и рендерим страницу с ошибками
                pass
        else:
            form = SpparstAddedForm()
            # Если GET или если форма НЕВАЛИДНА (is_valid == False)
            return render(request, 'telog_spparts/added_spparts.html', {
                'form_add_spparts': form})
    except ValueError:
        form = SpparstAddedForm()
        return render(request, 'telog_spparts/added_spparts.html', {
            'form_add_spparts': form,
            'error_added': 'Неверные данные. Попробуйте ещё раз',
        })
    return render(request, 'telog_spparts/added_spparts.html', {
        'form_add_spparts': form
    })


# Функционал калькулятора, работа с подгрузкой запчастей <select> из БД
def calc(request):
    # extra=1 означает, что изначально будет одна пустая строка
    RepairFormSet = formset_factory(CalcForm, extra=2)

    if request.method == 'POST':
        try:
            if 'clear' in request.POST:  # При нажатой кнопке с name="clear"
                return redirect('calculate')  # очиста данных

            calc_form = RepairFormSet(request.POST)
            if calc_form.is_valid():
                item_prices = []
                for form in calc_form:
                    ratio = form.cleaned_data.get('ratio', 1)
                    price = form.cleaned_data.get('price', 0)
                    if ratio >= 1:
                        item_price = price * ratio
                        item_prices.append(item_price)
                    # elif ratio == 1:
                    #     item_prices.append(price)
                    else:
                        item_price = 0
                        item_prices.append(item_price)
                # Считаем сумму всех введенных цен
                total_price = round(sum(item_prices), 2)  # float - 2 знака после ','
                t_price_rub = int(total_price)  # рубли - отброшен остаток (не округлён!!!)
                t_price_kop = int((total_price - t_price_rub) * 100)  # int(n * 100) - копеек
                # total_price = sum(form.cleaned_data.get('price', 0) for form in calc_form)
                return render(
                    request,
                    'telog_spparts/calc_page.html',
                    {
                        'calc_form': calc_form,
                        'total_price': t_price_rub,  # total_price
                        't_price_kop': t_price_kop,
                    })
            if not calc_form.is_valid():
                # Если форма невалидна (например, только зашли на страницу через POST),
                # создаем её заново с начальными значениями
                return redirect('calculate')  # очиста данных
        except TypeError:
            # Если ошибка заполнения полей, в частности - цены
            calc_form = RepairFormSet(request.POST)
            return render(
                request,
                'telog_spparts/calc_page.html',
                {'calc_form': calc_form,
                 'errors': 'Ошибка! Неверные данные! Проверьте заполнение поля цены и повторите попытку',
                 })
    else:  # если: request.method == 'GET'
        calc_form = RepairFormSet()
    return render(
        request,
        'telog_spparts/calc_page.html',
        {'calc_form': calc_form})
