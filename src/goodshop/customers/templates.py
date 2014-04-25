VENDOR_SUBJECT = """Order: #%(order_no)s from GoodShop"""
VENDOR_MSG = """
Hi %(vendor_first_name)s %(vendor_last_name)s, we have a new order for you!

OrderNo: #%(order_no)s
Date: %(date)s

Article details from order:
%(product_list)s

--------------------------------------------

Customer : %(customer_first_name)s %(customer_last_name)s
\tphone   : %(customer_phone)s
\te-mail  : %(customer_email)s
\taddress : %(customer_address)s

________________________________
"""
CUSTOMER_SUBJECT = """[GoodShop] Order created successfully"""
CUSTOMER_MSG = """
Dear %(customer_first_name)s %(customer_last_name)s, we have received your order and have notified the suppliers.
They will contact you soon.

Please find your order information below.
________________________________

OrderNo: #%(order_no)s
Date: %(date)s

Order details
%(product_list)s

Thanks for choosing GoodShop online store!
"""