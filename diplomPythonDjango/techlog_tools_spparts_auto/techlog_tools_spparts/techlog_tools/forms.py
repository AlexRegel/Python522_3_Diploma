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
            'description': 'Описание запчасти',
            'image': 'Изображение',
            'url': 'URL для заказа',
            'price_order': 'Примерная стоимость',
            'instructions': 'Инструкцию по установке',
            'datetime': 'Дата/время установки на авто',
            # 'date': 'Дата поступления в БД',
            # 'user_who_added': 'Пользователь добавивший в БД',
        }


# Форма переопределения для калькулятора
class TelogChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Здесь obj — это экземпляр модели TelogSpparts
        return f"{obj.title} (Цена: {obj.price_order})"


# Форма для калькулятьора (проверка со взаимодействием с БД)
class CalcForm(forms.Form):
    # Список запчастей (можно подгружать из БД)
    # item = forms.ChoiceField(
    #     choices=[('screen', 'Экран (1000-5000р)'), ('battery', 'АКБ (500-2000р)')],
    #     widget=forms.Select(attrs={'class': 'item-select'})
    # )
    # Список запчастей подгружаемых из БД
    item = TelogChoiceField(  # part
        queryset=TelogSpparts.objects.all(),  # choices
        label="Выберите деталь для рассчёта стоимости ремонта",
        empty_label="--- Запчасть/деталь не выбрана ---",
        # widget=forms.Select(attrs={'class': 'item-select'})
        required=False,  # параметр валидации, если поле пустое
    )
    # Поле для ввода точной цены пользователем
    price = forms.DecimalField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите цену', 'class': 'price-input'}),
        label="Укажите цену",
        required=False,  # если поле пустое, пройдёт валидацию
    )
    # Поле для ввода коэффициента-количества единиц запчастей
    ratio = forms.DecimalField(
        min_value=0,
        initial=1,  # Устанавливает значение по умолчанию
        help_text="Введите коэффициент",  # Опущен, если initial
        widget=forms.NumberInput(attrs={'placeholder': 'Введите коэффициент', 'class': 'ratio-input'}),
        label="Кол-во",  # Введите количество
    )
