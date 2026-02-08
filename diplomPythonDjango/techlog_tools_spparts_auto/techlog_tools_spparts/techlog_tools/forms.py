# from django.forms import ModelForm
from django import forms
from telog_spparts.models import Repairs, TelogSpparts
from django.core.exceptions import ValidationError


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
        # # Подсказка:
        # help_texts = {
        #     'priority_rep': 'приоритет ремонта -> ',
        # }


# Форма для добавления запчастей
class SpparstAddedForm(forms.ModelForm):
    class Meta:
        model = TelogSpparts
        fields = [
            'title', 'description', 'image', 'price_order',
            'url', 'product_code', 'instructions',  # 'datetime',
        ]
        labels = {
            'title': 'Наименование запчасти',
            'description': 'Описание запчасти',
            'image': 'Изображение',
            'price_order': 'Примерная стоимость',
            'url': 'URL для заказа',
            'product_code': 'Код товара/артикул',
            'instructions': 'Инструкцию по установке',
            # 'datetime': 'Дата/время установки на авто',
            # 'date': 'Дата поступления в БД',
            # 'user_who_added': 'Пользователь добавивший в БД',
        }

    # ВАЖНО!: __init__ должен быть на одном уровне с Meta, т.е. вне его!
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Принудительная установка типов полей (важно также -'datetime', если монтировать)
        self.fields['instructions'].widget = forms.TextInput(attrs={
            'placeholder': 'Выберите дату и время'})
        # - это упреждающее действие (чтобы браузер не изменил)

        # Вспомогательный текст для пользователя
        self.fields['title'].help_text = "Обязательно укажите полное название запчасти."

        # Установки полей (2-й вариант, в т.ч. необязательных)
        # и добавления плейсхолдеров, используя принцип неповторяемости:
        optional_data = {
            # 'datetime': 'Введите дату и время',
            'title': 'Введите наименование запчасти',
            'description': 'Необходимо подробное описание запчасти',
            # 'image': 'Изображение',
            'price_order': 'Введите ценовой порядок / интервал цен',
            'url': 'URL автомобильного интернет-магазина',
            'product_code': 'Введите код товара ',
            'instructions': 'Введите адрес инструкции (если доступна)',
        }
        for field_name, placeholder_text in optional_data.items():
            field = self.fields[field_name]
            # field.required = False
            # field.widget.attrs.update({'placeholder': placeholder_text})
            field.widget.attrs['placeholder'] = placeholder_text

        self.fields['instructions'].required = False

    # Имитация (вариация) ошибки заполнения формы
    def clean(self):
        # Получаем данные, которые уже прошли базовую проверку полей
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        product_code = cleaned_data.get("product_code")

        # Имитируем логическую ошибку всей формы
        if title and product_code and title.lower() == product_code.lower():
            raise ValidationError(
                # "Наименование запчасти не может быть идентично её коду! "
                # "Пожалуйста, введите корректные данные.",
                {'product_code': "Код продукта не может совпадать с названием!"}
            )
        # Передаем словарь: {имя_поля: сообщение_об_ошибке} для вывода частной ошибки по полю
        return cleaned_data


# Форма переопределения для калькулятора
class TelogChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Здесь obj — это экземпляр модели TelogSpparts
        return f"{obj.title} (Цена: {obj.price_order})"


# Форма для калькулятьора (проверка со взаимодействием с БД)
class CalcForm(forms.Form):
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
