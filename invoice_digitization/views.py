import logging
import uuid
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from invoice_digitization.serializers import CollectInvoiceSerializer, InvoiceStatusSerializer, UpdateInvoiceSerializer
from invoice_digitization.models import Invoice
from invoice_digitization.utilities.update_invoice import update_document
from invoice_digitization.utilities.invoice_details import get_invoice_details

logger = logging.getLogger(__name__)


class Ping(APIView):
    """
    This Ping API is used to test the working of a Django REST API
    """
    http_method_names = ['get']

    def get(self, request):
        return Response("Pong", status=status.HTTP_200_OK)


class CollectInvoiceView(APIView):
    serializer_class = CollectInvoiceSerializer
    http_method_names = ['post']

    def post(self, request):
        """
        This Post API collects invoice documents from end customers
        :param request:
        :return:
        """
        logger.info("CollectInvoiceView: starts execution")
        invoice_serializer = self.serializer_class(data=request.FILES)
        try:
            invoice_serializer.is_valid(raise_exception=True)
        except ValidationError as excep:
            logger.error("CollectInvoiceView: Error occurred: error::{}".format(str(excep)))
            resp = {
                'detail': excep.detail
            }
            return Response(resp, status=excep.status_code)

        validated_data = invoice_serializer.validated_data

        # Generate unique invoice number
        invoice_number = str(uuid.uuid4())
        logger.info("CollectInvoiceView: Created unique invoice number using uuid:{}".format(invoice_number))

        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            status=False,
            file_data=validated_data['file']
        )
        logger.info("CollectInvoiceView: Successfully created invoice:{}".format(invoice))

        resp = {
            "message": "invoice collected",
            "invoice_number": invoice_number
        }
        logger.info("CollectInvoiceView: Successfully collected invoice document")
        return Response(resp, status=status.HTTP_200_OK)


class InvoiceStatusView(APIView):
    serializer_class = InvoiceStatusSerializer
    http_method_names = ['get']

    def get(self, request):
        """
        This API is used to fetch the status (i.e. digitized or not) of a invoice (pdf)
        :param request:
        :return:
        """
        logger.info("InvoiceStatusView: starts execution")
        invoice_status_serializer = self.serializer_class(data=request.GET)
        try:
            invoice_status_serializer.is_valid(raise_exception=True)
        except ValidationError as excep:
            logger.error("InvoiceStatusView: Error occurred: error::{}".format(str(excep)))
            resp = {
                'detail': excep.detail
            }
            return Response(resp, status=excep.status_code)

        validated_data = invoice_status_serializer.validated_data

        invoice = Invoice.objects.get(invoice_number=validated_data['invoice_number'])
        invoice_status = invoice.status
        resp = {
            'invoice_number': validated_data['invoice_number'],
            'status': 'digitized' if invoice_status else 'not yet digitized'
        }
        logger.info("InvoiceStatusView: Successfully fetched the status of given invoice, details:{}".format(resp))
        return Response(resp, status=status.HTTP_200_OK)


class UpdateInvoiceView(APIView):
    serializer_class = UpdateInvoiceSerializer
    http_method_names = ['post']

    def post(self, request):
        """
        This Post API updates the invoice details.
        This API can be consumed by other micro-services or by internal users
        :param request:
        :return:
        """
        logger.info("CollectInvoiceView: starts execution")
        invoice_serializer = self.serializer_class(data=request.data)
        try:
            invoice_serializer.is_valid(raise_exception=True)
        except ValidationError as excep:
            logger.error("CollectInvoiceView: Error occurred: error::{}".format(str(excep)))
            resp = {
                'detail': excep.detail
            }
            return Response(resp, status=excep.status_code)

        validated_data = invoice_serializer.validated_data

        logger.info("UpdateInvoiceView: Requesting to update the invoice:{}".format(validated_data['invoice_number']))
        update_document(validated_data)
        logger.info("UpdateInvoiceView: Successfully updated the invoice:{}".format(validated_data['invoice_number']))

        resp = {
            "invoice_number": validated_data['invoice_number'],
            "details": "Successfully updated the invoice"
        }
        return Response(resp, status=status.HTTP_200_OK)


class InvoiceDetailsView(APIView):
    serializer_class = InvoiceStatusSerializer
    http_method_names = ['get']

    def get(self, request):
        """
        This API is used to fetch the details of an invoice.
        This API can be used by customers to view the structured details of given invoice
        :param request:
        :return:
        """
        logger.info("InvoiceDetailsView: starts execution")
        invoice_status_serializer = self.serializer_class(data=request.GET)
        try:
            invoice_status_serializer.is_valid(raise_exception=True)
        except ValidationError as excep:
            logger.error("InvoiceDetailsView: Error occurred: error::{}".format(str(excep)))
            resp = {
                'detail': excep.detail
            }
            return Response(resp, status=excep.status_code)

        validated_data = invoice_status_serializer.validated_data

        logger.info("InvoiceDetailsView: Requesting to fetch details of invoice:{}"
                    .format(validated_data["invoice_number"]))
        output = get_invoice_details(validated_data)
        resp = {
            'invoice_number': validated_data['invoice_number'],
            "details": output
        }
        logger.info("InvoiceDetailsView: Successfully completed the execution of InvoiceDetailsView")
        return Response(resp, status=status.HTTP_200_OK)
