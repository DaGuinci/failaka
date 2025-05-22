from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_permissions', 'username']  # Exclure les permissions utilisateur et le champ username

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if groups.count() > 1:
            raise forms.ValidationError("A user can only belong to one group.")
        return groups


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')  # Champs affichés dans le formulaire


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    form = UserAdminForm
    add_form = CustomUserCreationForm  # Utilise le formulaire personnalisé pour l'ajout
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_group')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Exclure les permissions utilisateur des formulaires
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Groups', {'fields': ('groups',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('password',)  # Rend le champ 'password' en lecture seule

    def get_group(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_group.short_description = 'Group'