"""
Pharmacy Core Module
====================

Base module for Pharmacy Management System (Mono-Pharmacie)

Author: Abdelghani Mehennaoui
Version: 17.0.1.0.0

Features:
---------
- Drug category hierarchical management
- Product extension for pharmaceutical products  
- Drug type classification (OTC, Prescription, Narcotic)
- Scientific name tracking
- Minimum stock quantity management
- Role-based access control (Admin, Sales, Stock Manager)
- Automatic lot tracking enforcement for all drugs

Technical Implementation:
------------------------
- Performance optimized with database indexes
- Parent-store for fast hierarchical queries
- Multi-language support (EN, FR, AR)
- Strict validation constraints
- Integration ready for pharmacy ecosystem modules

Dependencies:
------------
- base
- product
- uom

Related Modules:
---------------
- pharmacy_stock_lot: Lot and expiry management
- pharmacy_purchase: Purchase order management
- pharmacy_sales: Sales with auto-lot selection
- pharmacy_pos: Point of sale integration
- pharmacy_alerts: Automated notifications
- pharmacy_reports: Business intelligence

Installation Order: #1 (Install this first)

© 2026 Abdelghani Mehennaoui
"""

__version__ = '17.0.1.0.0'
__author__ = 'Abdelghani Mehennaoui'
__license__ = 'LGPL-3'
