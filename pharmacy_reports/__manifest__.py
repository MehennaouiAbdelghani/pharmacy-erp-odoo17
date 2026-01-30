# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy Reports',
    'version': '17.0.1.0.0',
    'category': 'Reporting/Pharmacy',
    'summary': 'Pharmacy business and regulatory reports',
    'description': """
        Pharmacy Reports Module
        =======================
        Comprehensive specific reports for pharmacy.
        
        Reports:
        * Expired drugs loss
        * Profit per product
        * Stock valuation
    """,
    'author': 'Abdelghani Mehennaoui',
    'depends': ['pharmacy_sales', 'pharmacy_purchase'],
    'data': [
        'views/pharmacy_report_menus.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
