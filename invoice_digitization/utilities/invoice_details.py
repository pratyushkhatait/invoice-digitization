import logging
from django.db.models import F, Sum
from invoice_digitization.models import Invoice, Product
logger = logging.getLogger(__name__)


def get_invoice_details(data):
    """
    This function fetch the details of a given invoice if the document is digitized
    :param data: invoice number
    :return: invoice details
    """
    logger.info('get_invoice_details: Started fetching the details of invoice:{}'.format(data['invoice_number']))

    invoice_query = Invoice.objects.filter(invoice_number=data['invoice_number'])
    invoice_status = invoice_query[0].status

    # If the invoice is not digitized, invoice details cannot see the invoice details
    if not invoice_status:
        logger.error("get_invoice_details: Invoice:{} is not digitized, cannot fetch it's details"
                     .format(data['invoice_number']))
        output = {
            "details": "Invoice is not digitized, cannot fetch it's details"
        }
        return output

    # Get all the products of a given invoice document
    product_query = Product.objects.filter(invoice__invoice_number=data['invoice_number'])
    products = list(product_query.values())

    output = {
        "invoice_details": list(invoice_query.values()),
        "product_details": products,
        "total_amount": product_query.aggregate(Sum('amount'))
    }
    logger.info("get_invoice_details: Successfully fetched the details:{} of invoice:{}"
                .format(output, data['invoice_number']))
    return output
