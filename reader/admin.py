# author: goodalg0s@gmail.com
from django.contrib import admin

from .models import (
    NemFile,
    Record100,
    Record250,
    Record550,
    ReaderRun,
    ReaderError,
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
        return False

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# + -  -  -  Inline  -  -  - +


class Record100_Inline(TabularInline_ReadOnly):
    model = Record100


class Record250_Inline(TabularInline_ReadOnly):
    model = Record250


class Record550_Inline(TabularInline_ReadOnly):
    model = Record550


class ReaderError_Inline(TabularInline_ReadOnly):
    model = ReaderError


# + -  -  -  Admin -  -  -  - +


@admin.register(NemFile)
class NemFile_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'id',
        'name',
        'description',
        'created_at',
    )

    search_fields = (
        'name',
    )

    inlines = [
        Record100_Inline,
        Record250_Inline,
        Record550_Inline
    ]


@admin.register(Record100)
class Record100_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'id',
        'nemfile',
        'record_indicator',
        'version_header',
        'datetime',
        'from_participant',
        'to_participant'
    )


@admin.register(Record250)
class Record250_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'id',
        'nemfile',
        'record_indicator',
        'nmi',
        'nmi_configuration',
        'register_id',
        'nmi_suffix',
        'mdm_data_stream_identifier',
        'meter_serial_number',
        'direction_indicator',
        'previous_register_read',
        'previous_register_read_datetime',
        'previous_quality_method',
        'previous_reason_code',
        'previous_reason_description',
        'current_register_read',
        'current_register_read_datetime',
        'current_quality_method',
        'current_reason_code',
        'current_reason_description',
        'quantity',
        'uom',
        'next_scheduled_read_date',
        'update_datetime',
        'msats_load_datetime'
    )

    search_fields = (
        'nmi',
        'meter_serial_number',
    )


@admin.register(Record550)
class Record550_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'id',
        'nemfile',
        'record_indicator',
        'previous_trans_code',
        'previous_ret_service_order',
        'current_trans_code',
        'current_ret_service_order'
    )


@admin.register(ReaderRun)
class ReaderRun_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'id',
        'status',
        'nemfile',
        'created_at',
    )

    inlines = (
        ReaderError_Inline,
    )

    search_fields = (
        'nemfile',
    )


@admin.register(ReaderError)
class ReaderError_Admin(ModelAdmin_ReadOnly):
    list_display = (
        'id',
        'reader_run',
        'description',
        'created_at',
    )
