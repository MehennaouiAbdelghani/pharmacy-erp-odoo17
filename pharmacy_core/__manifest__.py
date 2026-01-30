# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy Core',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Pharmacy',
    'summary': 'Base pharmacy configuration and master data management',
    'description': """
        Pharmacy Core Module
        ====================
        Base pharmacy configuration and master data management.
        
        Features:
        ---------
        * Drug category management
        * Product extension for pharmacy products
        * Drug classification (OTC, Prescription, Narcotic)
        * Scientific name tracking
        * Minimum quantity thresholds
        
        Author: Abdelghani Mehennaoui
        
        This module is part of the Pharmacy Management System (Mono-Pharmacie).
    """,
    'author': 'Abdelghani Mehennaoui',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'product', 'uom'],
    'data': [
        'security/pharmacy_security.xml',
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/pharmacy_drug_category_views.xml',
        'views/pharmacy_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
