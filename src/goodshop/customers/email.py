from django.core.mail import send_mail
from project.settings import EMAIL_HOST
from . import templates

def email_order_notification(order):
    sales = order.sales_by_vendor()
    customer = order.get_customer_profile()

    ## Info to replace in the templates
    LABELS = {}

    # General order info
    LABELS['order_no'] = order.pk
    LABELS['date'] = order.get_date()
    LABELS['order_total'] = order.total_price

    # Customer info
    LABELS['customer_first_name'] = customer.user.first_name
    LABELS['customer_last_name'] = customer.user.last_name
    LABELS['customer_phone'] = order.get_customer_phone()
    LABELS['customer_email'] = customer.user.email
    LABELS['customer_address'] = customer.address

    # Variable info
    LABELS['product_list'] = ''
    LABELS['vendor_first_name'] = ''
    LABELS['vendor_last_name'] = ''


    ## Send vendor e-mail
    for vendor_id in sales:
        ## Variable information in the message
        p_list = order.get_product_report(sales[vendor_id])
        a_prod_in_ord = sales[vendor_id][0]
        vendor = a_prod_in_ord.product.vendor
        vendor_email = vendor.email

        LABELS['product_list'] = p_list.replace('\n', '\n\t')
        LABELS['vendor_first_name'] = vendor.first_name
        LABELS['vendor_last_name'] = vendor.last_name

        send_mail(templates.VENDOR_SUBJECT % (LABELS),
                  templates.VENDOR_MSG     % (LABELS),
                  EMAIL_HOST,
                  [vendor_email, 'coca_lp@hotmail.com', 'haibrayn@hotmail.com'],
                  fail_silently=False
                  )


    ## Send customer e-mail
    order_prods = order.get_order_products()
    p_list = order.get_product_report(order_prods)
    LABELS['product_list'] = p_list.replace('\n', '\n\t')

    send_mail(templates.CUSTOMER_SUBJECT % LABELS,
              templates.CUSTOMER_MSG % LABELS,
              EMAIL_HOST,
              [customer.user.email, 'coca_lp@hotmail.com', 'haibrayn@hotmail.com'],
              fail_silently=False
              )