# author: goodalg0s@gmail.com
from django.contrib import admin

from .models import (
    NemFile
)


class ModelAdmin_ReadOnly(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class TabularInline_ReadOnly(admin.TabularInline):
    can_delete = True
    show_change_link = True
    extra = 0

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# + -  -  -  -  -  -  - +

@admin.register(NemFile)
class NemFile_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'name',
        'description',
        'created_at',
    )

    search_fields = (
        'name',
    )
