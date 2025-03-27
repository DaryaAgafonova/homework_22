from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Импортируем User из users.models

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'country')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'country')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'country')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('username', 'first_name', 'last_name', 'avatar', 'phone_number', 'country')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    
    ordering = ('email',)