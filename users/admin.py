from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from users.models import UserProfile

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_client']

    fieldsets = UserAdmin.fieldsets + (
        ('store', {'fields': ('is_client', 'is_vendor', 'is_moderator')}),
    )



admin.site.register(CustomUser, CustomUserAdmin)

#admin.site.register(UserProfile)
