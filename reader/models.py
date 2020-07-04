# author: goodalg0s@gmail.com

from django.db import models

ALLOWED_RECORD_INDICATOR = (
    ('100', '100'),
    ('250', '250'),
    ('550', '550'),
)

ALLOWED_VERSION_HEADER = (
    # 'NEM12',
    ('NEM13', 'NEM13'),
)

ALLOWED_DIRECTION_INDICATOR = (
    ('I', 'Import'),  # ‘I’ = Import to grid
    ('E', 'Export'),  # ‘E’ = Export from grid
)

MAX_LENGTH_FILE_NAME = 400


class NemFile(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_FILE_NAME,
        blank=False,
        unique=True
    )
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Record100(models.Model):
    record_indicator = models.CharField(
        max_length=3,
        blank=False,
        choices=ALLOWED_RECORD_INDICATOR
    )
    version_header = models.CharField(
        max_length=5,
        blank=False,
        choices=ALLOWED_VERSION_HEADER
    )
    datetime = models.DateTimeField()
    from_participant = models.CharField(max_length=10)
    to_participant = models.CharField(max_length=10)

    nemfile = models.ForeignKey(
        NemFile,
        blank=False,
        null=False,
        related_name='record100',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('nemfile', 'record_indicator')


class Record250(models.Model):

    record_indicator = models.CharField(
        max_length=3,
        blank=False,
        choices=ALLOWED_RECORD_INDICATOR
    )
    nmi = models.CharField(max_length=10)
    nmi_configuration = models.CharField(max_length=240)
    register_id = models.CharField(max_length=10)
    nmi_suffix = models.CharField(max_length=2)

    mdm_data_stream_identifier = models.CharField(max_length=2)
    meter_serial_number = models.CharField(max_length=12)
    direction_indicator = models.CharField(
        max_length=1,
        choices=ALLOWED_DIRECTION_INDICATOR
    )

    previous_register_read = models.CharField(max_length=15)
    previous_register_read_datetime = models.DateTimeField()
    previous_quality_method = models.CharField(max_length=3)
    previous_reason_code = models.IntegerField()
    previous_reason_description = models.CharField(max_length=240)

    current_register_read = models.CharField(max_length=15)
    current_register_read_datetime = models.DateTimeField()
    current_quality_method = models.CharField(max_length=3)
    current_reason_code = models.IntegerField()
    current_reason_description = models.CharField(max_length=240)

    quantity = models.IntegerField()
    uom = models.CharField(max_length=5)
    next_scheduled_read_date = models.DateField()
    update_datetime = models.DateTimeField()
    msats_load_datetime = models.DateTimeField()

    nemfile = models.ForeignKey(
        NemFile,
        blank=False,
        null=False,
        related_name='record250',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('nemfile', 'record_indicator')


class Record550(models.Model):
    record_indicator = models.CharField(
        max_length=3,
        blank=False,
        choices=ALLOWED_RECORD_INDICATOR
    )
    previous_trans_code = models.CharField(max_length=1)
    previous_ret_service_order = models.CharField(max_length=15)
    current_trans_code = models.CharField(max_length=1)
    current_ret_service_order = models.CharField(max_length=15)

    nemfile = models.ForeignKey(
        NemFile,
        blank=False,
        null=False,
        related_name='record550',
        on_delete=models.CASCADE
    )

    record250 = models.ForeignKey(
        Record250,
        blank=False,
        null=False,
        related_name='record550',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('nemfile', 'record_indicator')


class ReaderRun(models.Model):
    ''' Store information of every run of NEM file reader '''

    STATUSES = (
        ('S', 'Successful'),
        ('F', 'Failed'),
    )

    status = models.CharField(max_length=1, choices=STATUSES)
    created_at = models.DateTimeField(auto_now=True)
    nemfile = models.ForeignKey(
        NemFile,
        blank=False,
        null=False,
        related_name='runs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nemfile.__str__() + self.created_at


class ReaderError(models.Model):
    ''' Store any error occured during the reader run '''

    reader_run = models.ForeignKey(
        ReaderRun,
        blank=False,
        null=False,
        related_name='errors',
        on_delete=models.CASCADE
    )

    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reader_run + ': ' + self.description
