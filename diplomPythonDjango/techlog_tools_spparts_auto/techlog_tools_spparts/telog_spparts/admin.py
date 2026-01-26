from django.contrib import admin
from .models import TelogSpparts, Repairs


#  Для отображения в админке скрытых полей
# используются только зарезервированные св-ва
class RepairsAdmin(admin.ModelAdmin):
    #  Здесь зарез-е св-во 'readonly_fields':
    readonly_fields = ('date_creation',)


class TelogSppartsAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(TelogSpparts, TelogSppartsAdmin)
admin.site.register(Repairs, RepairsAdmin)
