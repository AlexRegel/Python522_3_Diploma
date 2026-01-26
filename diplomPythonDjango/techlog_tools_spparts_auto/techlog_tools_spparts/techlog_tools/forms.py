# from django.forms import ModelForm
from django import forms
from telog_spparts.models import Repairs, TelogSpparts


# Форма для добавления ремонтов
class RepairsForm(forms.ModelForm):
    class Meta:
        model = Repairs
        fields = ['title', 'rep_memo', 'priority_rep']
        labels = {
            'title': 'Наименование ремонта',
            'rep_memo': 'Описание ремонта',
            'priority_rep': 'Укажите приоритет ремонта',
        }
        # Подсказка:
        # help_texts = {
        #     'priority_rep': 'приоритет ремонта -> ',
        # }


# Форма для добавления запчастей
class SpparstAddedForm(forms.ModelForm):
    class Meta:
        model = TelogSpparts
        fields = [
            'title',
            'description',
            'image',
            'price_order',
            'url',
            'product_code',
            'datetime',
            'instructions',
        ]
        labels = {
            'title': 'Наименование запчасти',
            'description': 'Описание',
            'image': 'Изображение',
            'url': 'url для заказа',
            'price_order': 'Примерная стоимость',
            'instructions': 'Инструкцию по установке (если есть)',
            'datetime': 'Отметьте, дату/время установки на авто',
            # 'date': 'Дата поступления в БД',
            # 'user_who_added': 'Пользователь добавивший в БД',
        }


# Форма переопределения для калькулятора
class TelogChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Здесь obj — это экземпляр модели TelogSpparts
        return f"{obj.title} (Цена: {obj.price_order})"


# Форма для калькулятьора (пока без взаимодействия с БД)
# class CalcForm(forms.Form):
#     # Поле для выбора одного объекта из базы (по умолчанию)
#     # part = forms.ModelChoiceField(
#     #     queryset=TelogSpparts.objects.all(),
#     #     label="Выберите деталь",
#     #     empty_label="--- Деталь не выбрана ---"
#     # )
#     part = TelogChoiceField(
#         queryset=TelogSpparts.objects.all(),
#         label="Выберите деталь",
#         empty_label="--- Деталь не выбрана ---"
#     )
#     # ориентировочная цена запчасти
#     # Поле, где пользователь сам уточнит цену на основе увиденного интервала
#     chosen_price = forms.DecimalField(
#         label="Укажите точную цену из интервала",
#         min_value=0
#     )
#
#     number1 = forms.FloatField(label="Число 1")
#     number2 = forms.FloatField(label="Число 2")
#     operation = forms.ChoiceField(
#         choices=[
#             ('add', '+'),
#             ('sub', '-'),
#             ('mul', '*'),
#             ('div', '/'),
#         ],
#         label="Операция",
#         initial='add',
#         widget=forms.RadioSelect,
#     )

# Форма для калькулятьора (проверка со взаимодействием с БД)
class CalcForm(forms.Form):  # либо RepairItemForm
    # Список запчастей (можно подгружать из БД)
    # item = forms.ChoiceField(
    #     choices=[('screen', 'Экран (1000-5000р)'), ('battery', 'АКБ (500-2000р)')],
    #     widget=forms.Select(attrs={'class': 'item-select'})
    # )
    # Список запчастей подгружаемых из БД
    item = TelogChoiceField(  # part
        queryset=TelogSpparts.objects.all(),  # choices
        label="Выберите деталь",
        empty_label="--- Запчасть/деталь не выбрана ---",
        # widget=forms.Select(attrs={'class': 'item-select'})
    )
    # Поле для ввода точной цены пользователем
    price = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите цену', 'class': 'price-input'}),
        # label="Укажите точную цену (из интервала)",
    )
