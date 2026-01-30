# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy Stock Lot Management',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Pharmacy',
    'summary': 'Lot tracking, expiry management, and FIFO enforcement for pharmacy',
    'description': """
        Pharmacy Stock Lot Management
        ==============================
        Advanced lot tracking and expiry date enforcement for pharmaceutical products.
        
        Features:
        ---------
        * Expiry date tracking per lot
        * Automatic expired lot detection
        * FIFO (First In, First Out) enforcement
        * Alert threshold management per lot
        * Block sales of expired products
        * Configurable expiry alert thresholds
        
        Author: Abdelghani Mehennaoui
        
        This module extends pharmacy_core with lot and expiry management.
    """,
    'author': 'Abdelghani Mehennaoui',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['stock', 'product_expiry', 'pharmacy_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_lot_views.xml',
        'views/stock_move_line_views.xml',
        'views/product_template_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 2,
}
