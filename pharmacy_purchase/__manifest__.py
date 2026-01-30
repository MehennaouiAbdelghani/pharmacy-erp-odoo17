# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy Purchase Management',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Pharmacy',
    'summary': 'Controlled drug purchasing with mandatory lot and expiry tracking',
    'description': """
        Pharmacy Purchase Management
        =============================
        Controlled purchasing process for pharmaceutical products.
        
        Features:
        ---------
        * Mandatory lot assignment on purchase receipt
        * Mandatory expiry date entry
        * Block receipt without expiry date
        * Integration with stock lot management
        
        Author: Abdelghani Mehennaoui
    """,
    'author': 'Abdelghani Mehennaoui',
    'license': 'LGPL-3',
    'depends': ['purchase', 'pharmacy_stock_lot'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 3,
}
