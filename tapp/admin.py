from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Entry, SelledItems, Storage

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'arabic_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'role')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'arabic_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'arabic_name', 'role'),
        }),
    )
    
    search_fields = ('username', 'email', 'arabic_name')
    filter_horizontal = ()

admin.site.register(Entry)
admin.site.register(Storage)
admin.site.register(SelledItems)
admin.site.register(CustomUser, CustomUserAdmin)
