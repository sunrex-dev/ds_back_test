from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class MyUserAdmin(UserAdmin):
    # 「まずユーザー名とパスワードを登録してください。」の文言を非表示にする
    add_form_template = None
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('テナント情報'), {'fields': ('tenant_id',)}),
        #(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'tenant_id'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    #list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_display = ('email', 'tenant_id', 'full_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'tenant_id')
    #search_fields = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'full_name')
    ordering = ('tenant_id', 'email',)


admin.site.register(User, MyUserAdmin)
