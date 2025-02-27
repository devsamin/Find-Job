from django.contrib import admin
from . import models

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'created_at']
admin.site.register(models.ContactMessage, ContactModelAdmin)