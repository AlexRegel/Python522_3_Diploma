from django.db import models


# Модель Техучёта запчастей
# spare parts - запчасти.
class TelogSpparts(models.Model):
    title = models.CharField(max_length=100)  # Наименование запчасти.
    description = models.TextField()  # Её описание
    image = models.ImageField(upload_to='techlog_tools/images_spparts/')  # Её изображение
    price_order = models.CharField(max_length=50)  # Цена / Порядок цены
    url = models.URLField(blank=True)  # url заказа (не обязательное для заполнения)
    product_code = models.CharField(max_length=70)  # код продукта
    date = models.DateField()  # Дата поступления в базу
    datetime = models.DateTimeField(null=True, blank=True)  # Дата/время установки на авто необ.

    # Код продукта, артикул или sku - Stock Keeping Unit (единица складского учета)

    def __str__(self):
        return self.title
