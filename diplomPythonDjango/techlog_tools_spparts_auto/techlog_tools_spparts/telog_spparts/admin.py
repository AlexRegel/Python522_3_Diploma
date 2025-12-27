from django.contrib import admin
from .models import TelogSpparts, Repairs


class RepairsAdmin(admin.ModelAdmin):
    #  Для отображения в админке скрытых полей
    #  Используем следующее зарезервированное свойство
    readonly_fields = ('date_creation',)


admin.site.register(TelogSpparts)
admin.site.register(Repairs, RepairsAdmin)
