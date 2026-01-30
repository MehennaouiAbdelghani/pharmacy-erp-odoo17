# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy Sales Management',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Pharmacy',
    'summary': 'Drug sales with automatic lot selection (FIFO) and profit tracking',
    'description': """
        Pharmacy Sales Management
        ==========================
        Advanced sales management for pharmaceutical products.
        
        Features:
        ---------
        * Automatic lot selection (nearest expiry / FIFO)
        * Block negative stock sales
        * Profit calculation per sale line
        * Integration with stock lot management
        * All sales linked to lots
        
        Author: Abdelghani Mehennaoui
    """,
    'author': 'Abdelghani Mehennaoui',
    'license': 'LGPL-3',
    'depends': ['sale_management', 'sale_stock', 'pharmacy_stock_lot'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 4,
}
