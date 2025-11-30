from django.db import models


class TechlogTools(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='techlog_tools/images/')
    url = models.URLField(blank=True)  # Поле не обязательное для заполнения

    def __str__(self):
        return self.title
