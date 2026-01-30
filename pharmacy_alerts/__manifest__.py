# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy Alerts & Notifications',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Pharmacy',
    'summary': 'Automated alerts for expiry, low stock, and dead stock',
    'description': """
        Pharmacy Alerts & Notifications
        ================================
        Automated notification system for pharmacy management.
        
        Features:
        ---------
        * Daily expiry alerts (02:00)
        * Daily low stock alerts (02:00)
        * Monthly dead stock detection
        * Activity creation for managers
        * Email notifications
        
        Author: Abdelghani Mehennaoui
    """,
    'author': 'Abdelghani Mehennaoui',
    'license': 'LGPL-3',
    'depends': ['mail', 'pharmacy_stock_lot'],
    'data': [
        'data/pharmacy_cron_jobs.xml',
        'views/pharmacy_alert_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 6,
}
