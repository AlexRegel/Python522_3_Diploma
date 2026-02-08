from django.db import models


# Модель инструмента (на главной)
class TechlogTools(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='techlog_tools/images/')
    url = models.URLField(blank=True)  # Поле не обязательное для заполнения

    def __str__(self):
        return self.title


# Модель техучёта инструмента в разделе Интрументы
class TechlogTools2(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(blank=True)
    image = models.ImageField(upload_to='techlog_tools/images/')
    url = models.URLField(blank=True)  # Поле не обязательное для заполнения

    # Для строкового представления объекта (в админке):
    def __str__(self):
        return self.title
        # Если дату, любым способом:
        # return str(self.date)
        # return f"{self.date}", но до миграций
