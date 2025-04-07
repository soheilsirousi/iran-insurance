from django.contrib import admin

from log.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'operation', 'created_time')
