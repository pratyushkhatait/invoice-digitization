from django.db import models
from django.utils import timezone
from invoice_digitization.config import INVOICE_STORAGE_PATH


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    issue_date = models.DateTimeField(default=timezone.now)
    from_client = models.CharField(max_length=50, blank=True, null=True)
    for_client = models.CharField(max_length=50, blank=True, null=True)
    file_data = models.FileField(upload_to=INVOICE_STORAGE_PATH)

    class Meta:
        managed = True
        db_table = 'invoice'

    def __str__(self):
        return str(self.invoice_number)


class Product(models.Model):
    item = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'product'

    def __str__(self):
        return str(self.item)
