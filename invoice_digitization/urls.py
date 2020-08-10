from django.conf.urls import url
from invoice_digitization.views import (Ping, CollectInvoiceView,
                                        InvoiceStatusView, UpdateInvoiceView,
                                        InvoiceDetailsView)

urlpatterns = [
    # Ping Pong API
    url(r'^ping/$', Ping.as_view(), name='ping'),
    # Collect invoice from end customer
    url(r'^collect-invoice/$', CollectInvoiceView.as_view(), name='collect-invoice'),
    # Status of an invoice
    url(r'^invoice-status/$', InvoiceStatusView.as_view(), name='invoice-status'),
    # Update invoice data
    url(r'^update-invoice/$', UpdateInvoiceView.as_view(), name='update-invoice'),
    # Details of an invoice
    url(r'^invoice-details/$', InvoiceDetailsView.as_view(), name='invoice-details'),
]
