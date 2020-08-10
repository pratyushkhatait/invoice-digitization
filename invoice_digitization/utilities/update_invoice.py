import logging
from invoice_digitization.models import Invoice, Product
logger = logging.getLogger(__name__)


def update_document(data):
    """
    This function updates the details of an invoice.
    Internal users or other micro-services
    :param data:
    :return:
    """
    logger.info('update_document: Document updation started with data:{}'.format(data))
    try:
        invoice = Invoice.objects.get(invoice_number=data['invoice_number'])
    except Invoice.DoesNotExist:
        logger.error("update_document: invoice number={} not found".format(data['invoice_number']))
        return

    if data.get('status'):
        invoice.status = data['status']
    if data.get('from_client'):
        invoice.from_client = data['from_client']
    if data.get('for_client'):
        invoice.for_client = data['for_client']
    if data.get('products'):
        for product in data['products']:
            try:
                p = Product.objects.get(item=product['item'])
                p.quantity = product['quantity']
                p.unit_price = product['unit_price']
                p.amount = product['quantity'] * product['unit_price']
                p.invoice = invoice
                p.save()
                logger.info("update_document: updated the product")
            except Product.DoesNotExist:
                Product.objects.create(
                    item=product['item'],
                    quantity=product['quantity'],
                    unit_price=product['unit_price'],
                    amount=product['quantity']*product['unit_price'],
                    invoice=invoice
                )
                logger.info("update_document: Created the product")
    invoice.save()
    logger.info("update_document: Successfully updated invoice:{}".format(data['invoice_number']))
