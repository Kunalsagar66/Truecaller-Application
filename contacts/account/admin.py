# Django modules
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm


# Django locals
from .models import Account, UserToken

class AccountAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    model = Account

    list_display = ('username', 'name', 'phone_number', 'is_spam', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('username', 'name', 'phone_number')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'name', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin'),
        }),
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(UserToken)


