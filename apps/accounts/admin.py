from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important dates', {
                'fields': ('last_login', 'date_joined', 'last_activity')
            }
        ),
    )
    readonly_fields = ('last_login', 'date_joined', 'last_activity')
    save_on_top = True
    save_as = True


admin.site.site_title = 'Social Network'
admin.site.site_header = 'Social Network'
