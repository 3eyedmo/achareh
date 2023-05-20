from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
User = get_user_model()


admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['id', 'phone_number', 'is_admin', 'is_active']
    list_filter = ['is_admin', 'is_active']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', )}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2')}
        ),
    )
    search_fields = ['phone_number']
    ordering = ['phone_number']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

