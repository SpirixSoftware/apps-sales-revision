# -*- coding: utf-8 -*-
# Copyright (C) 2025 Spirix Software
# This file is part of a proprietary Odoo addon developed by Spirix Software
# License OPL-1 (Odoo Proprietary License v1.0)

{
    'name': 'Sales Quotation/Order Revision',
    'version': '19.0.1.0.0',
    'summary': 'Allows users to revise sales quotations/orders and track their history.',
    'category': 'Sales',
    'author': 'Spirix Software',
    'company': 'Spirix Software',
    'maintainer': 'Spirix Software',
    'website': 'https://spirixsoftware.in/',
    'depends': [
        'sale_management'
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'license': 'OPL-1',
    'price': 7.80,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
}