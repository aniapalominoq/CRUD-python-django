from django.contrib import admin
from .models import Notes


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

    # Register your models here.
admin.site.register(Notes, NoteAdmin)
