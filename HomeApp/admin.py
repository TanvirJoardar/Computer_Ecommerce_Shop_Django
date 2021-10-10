from django.contrib import admin
from HomeApp.models import Setting, ContactMessage

# Register your models here.


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'phone', 'image_tag']
    list_filter = ['title']
    list_per_page = 5
    search_fields = ['title']


admin.site.register(Setting, SettingAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    list_filter = ['email']
    list_per_page = 5
    search_fields = ['email']


admin.site.register(ContactMessage, ContactAdmin)
