from django.contrib import admin
from .models import User, Contact, SpamMark


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email', 'date_of_birth', 'date_joined')
    search_fields = ('username', 'phone_number', 'email')
    list_filter = ('date_joined',)
    readonly_fields = ('date_joined', 'last_login')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'phone_number', 'email', 'is_favorite')
    search_fields = ('name', 'phone_number', 'email')
    list_filter = ('owner', 'is_favorite')

