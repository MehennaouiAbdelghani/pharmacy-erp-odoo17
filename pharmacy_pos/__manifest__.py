# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy POS Integration',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Pharmacy',
    'summary': 'POS integration with FIFO and expiry enforcement',
    'description': """
        Pharmacy POS Integration
        ========================
        Point of Sale integration for pharmacy with all safety features.
        
        Features:
        ---------
        * FIFO enforcement in POS
        * Expiry date validation
        * Fast barcode scanning
        * Same rules as backend sales
        
        Author: Abdelghani Mehennaoui
    """,
    'author': 'Abdelghani Mehennaoui',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'pharmacy_sales'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pharmacy_pos/static/src/js/pharmacy_pos.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 5,
}
