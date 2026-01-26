from django.db import models
from django.contrib.auth.models import User


# Модель Техучёта запчастей
# spare parts - запчасти.
class TelogSpparts(models.Model):
    title = models.CharField(max_length=100)  # Наименование запчасти.
    description = models.TextField()  # Её описание
    image = models.ImageField(upload_to='techlog_tools/images_spparts/')  # Её изображение
    price_order = models.CharField(max_length=50)  # Цена / Порядок цены
    url = models.URLField(blank=True)  # url заказа (не обязательное для заполнения)
    product_code = models.CharField(max_length=70)  # код продукта
    date = models.DateField(auto_now_add=True)  # Дата поступления в базу
    datetime = models.DateTimeField(null=True, blank=True)  # Дата/время установки на авто необ.
    instructions = models.CharField(max_length=100, null=True,
                                    blank=True)  # стат-ссылка, если есть инструкция (не обязательное для заполнения)
    # user_who_added = models.ForeignKey(  # performer - пользователь_исполнитель
    #     User,
    #     on_delete=models.SET_NULL,
    #     null=True,  # Обязательно для SET_NULL
    #     blank=True  # Позволяет оставлять поле пустым
    #     # в формах/админке
    # )

    # Код продукта, артикул или sku - Stock Keeping Unit (единица складского учета)

    def __str__(self):
        return self.title


# def get_default_user():
#     # Ищем пользователя 'deleted_user', если его нет — создаем
#     user, created = User.objects.get_or_create(username='deleted_user')
#     return user.pk


# # repairs / routine repairs -
# # - модель ремонты / текущие ремонты
class Repairs(models.Model):
    title = models.CharField(max_length=100)  # , verbose_name="Наименование ремонта"
    rep_memo = models.TextField(blank=True)  # его описание (записка)
    date_creation = models.DateTimeField(auto_now_add=True)  # Создано
    ready = models.DateTimeField(blank=True, null=True)  # Завершено
    priority_rep = models.BooleanField(default=False)  # Приоритет
    user_performer = models.ForeignKey(  # performer - пользователь_исполнитель
        User,
        on_delete=models.SET_NULL,
        null=True,  # Обязательно для SET_NULL
        blank=True  # Позволяет оставлять поле пустым
        # в формах/админке
    )

    def __str__(self):
        return self.title

