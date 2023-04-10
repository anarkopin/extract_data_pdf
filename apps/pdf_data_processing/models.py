from django.db import models
from simple_history.models import HistoricalRecords


class TaxFiling(models.Model):
    identificador = models.CharField(max_length=255)
    tax_filing = models.CharField(max_length=255)
    wages = models.IntegerField( )
    total_deductions = models.IntegerField()
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     verbose_name="created by",
    #     related_name="tax_filings",
    # )
    historical = HistoricalRecords()
