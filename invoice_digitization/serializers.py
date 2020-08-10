import logging
from rest_framework import serializers
from invoice_digitization.models import Invoice
logger = logging.getLogger(__name__)


class CustomBaseSerializer(serializers.Serializer):

    def validate(self, data):
        return super().validate(data)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CollectInvoiceSerializer(CustomBaseSerializer):
    file = serializers.FileField(required=True)


class InvoiceStatusSerializer(CustomBaseSerializer):
    invoice_number = serializers.CharField(max_length=50, required=True)

    def validate(self, data):
        try:
            Invoice.objects.get(invoice_number=data['invoice_number'])
        except Invoice.DoesNotExist:
            logger.error("InvoiceStatusSerializer: invoice with invoice number:{} does not exist"
                         .format(data['invoice_number']))
            raise serializers.ValidationError(detail="invoice not found")
        return data


class UpdateInvoiceSerializer(CustomBaseSerializer):
    invoice_number = serializers.CharField(max_length=50, required=True)
    status = serializers.BooleanField(required=False)
    from_client = serializers.CharField(max_length=50, required=False)
    for_client = serializers.CharField(max_length=50, required=False)
    products = serializers.ListField(child=serializers.JSONField(required=True))

    def validate(self, data):
        try:
            Invoice.objects.get(invoice_number=data['invoice_number'])
        except Invoice.DoesNotExist:
            logger.error("InvoiceStatusSerializer: invoice with invoice number:{} does not exist"
                         .format(data['invoice_number']))
            raise serializers.ValidationError(detail="invoice not found")
        return data
