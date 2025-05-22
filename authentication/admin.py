from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from .models import User


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if groups.count() > 1:
            raise forms.ValidationError("A user can only belong to one group.")
        return groups


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    form = UserAdminForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_group')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_group(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_group.short_description = 'Group'