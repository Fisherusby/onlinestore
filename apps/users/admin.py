from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import CustomUser
from apps.wallet.models import Wallet

# from users.models import UserProfile


class WalletInLine(admin.StackedInline):
    model = Wallet
    can_delete = False
    verbose_name_plural = 'Wallet'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (WalletInLine,)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_client']

    fieldsets = UserAdmin.fieldsets + (('store', {'fields': ('is_client', 'is_vendor', 'is_moderator')}),)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.register(UserProfile)
