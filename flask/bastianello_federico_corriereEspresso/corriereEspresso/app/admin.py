from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from app.models import (
    BaseDataUser, Clienti, Consegna
)

from django.contrib.auth.models import Group, Permission

operatore, _ = Group.objects.get_or_create(name="Operatore")
admin_group, _ = Group.objects.get_or_create(name="Admin")


operatore.permissions.set([
    Permission.objects.get(codename="view_clienti"),
    Permission.objects.get(codename="add_clienti"),
    Permission.objects.get(codename="change_clienti"),

    Permission.objects.get(codename="view_consegna"),
    Permission.objects.get(codename="add_consegna"),
    Permission.objects.get(codename="change_consegna"),
])


admin_group.permissions.set([
    Permission.objects.get(codename="view_basedatauser"),
    Permission.objects.get(codename="add_basedatauser"),
    Permission.objects.get(codename="change_basedatauser"),
    Permission.objects.get(codename="delete_basedatauser"),

    *operatore.permissions.all(),
])


@admin.register(BaseDataUser)
class CustomUserAdmin(UserAdmin):
    model = BaseDataUser

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informazioni personali", {
            "fields": ("first_name", "last_name", "email")
        }),
        ("Permessi base", {
            "fields": ("is_active", "is_staff")
        }),
        ("Date importanti", {
            "fields": ("last_login", "date_joined")
        }),
        ("Permessi", {
            "fields": ("groups",)
        })
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "first_name",
                "last_name",
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "groups"
            ),
        }),
    )

    filter_horizontal = ("groups",)


@admin.register(Clienti)
class ClientiAdmin(admin.ModelAdmin):
    list_display = ("user", "comune", "provincia")


@admin.register(Consegna)
class ConsegnaAdmin(admin.ModelAdmin):
    list_display = ("chiaveConsegna", "cliente", "stato", "dataRitiro")

