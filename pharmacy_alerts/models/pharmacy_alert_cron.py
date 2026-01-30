# -*- coding: utf-8 -*-

from odoo import models, api
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)


class PharmacyAlertCron(models.TransientModel):
    """Pharmacy Alert Cron Handler
    
    Contains all scheduled alert logic for pharmacy management.
    Optimized for performance with batch processing.
    
    Author: Abdelghani Mehennaoui
    """
    _name = 'pharmacy.alert.cron'
    _description = 'Pharmacy Alert Cron Handler'

    @api.model
    def cron_expiry_alert(self):
        """
        Daily Cron (02:00): Check for near-expiry lots
        Creates activities for pharmacy admin
        """
        _logger.info("Starting expiry alert cron job...")
        
        today = date.today()
        
        # Find lots with warning status (near expiry or expired)
        lots_warning = self.env['stock.lot'].search([
            ('is_drug_lot', '=', True),
            ('alert_status', 'in', ['warning', 'expired']),
            ('product_qty', '>', 0),  # Only lots with remaining stock
        ])
        
        if not lots_warning:
            _logger.info("No lots near expiry found")
            return
        
        # Get pharmacy admin users
        admin_group = self.env.ref('pharmacy_core.group_pharmacy_admin')
        admin_users = admin_group.users
        
        # Create activities for each lot
        for lot in lots_warning:
            days_until_expiry = lot.days_until_expiry
            
            if lot.expired:
                summary = f"EXPIRED: {lot.product_id.name} - Lot {lot.name}"
                note = f"""
                    <p><strong>⚠️ EXPIRED LOT DETECTED</strong></p>
                    <ul>
                        <li>Product: {lot.product_id.name}</li>
                        <li>Lot: {lot.name}</li>
                        <li>Expiry Date: {lot.expiration_date}</li>
                        <li>Quantity Remaining: {lot.product_qty}</li>
                    </ul>
                    <p><strong>Action Required:</strong> Remove from saleable stock immediately.</p>
                """
            else:
                summary = f"Near Expiry: {lot.product_id.name} - {days_until_expiry} days left"
                note = f"""
                    <p><strong>⚠ EXPIRY WARNING</strong></p>
                    <ul>
                        <li>Product: {lot.product_id.name}</li>
                        <li>Lot: {lot.name}</li>
                        <li>Expiry Date: {lot.expiration_date}</li>
                        <li>Days Until Expiry: {days_until_expiry}</li>
                        <li>Quantity Remaining: {lot.product_qty}</li>
                    </ul>
                    <p><strong>Action Required:</strong> Prioritize sale or consider return to supplier.</p>
                """
            
            for user in admin_users:
                self.env['mail.activity'].create({
                    'res_id': lot.id,
                    'res_model_id': self.env.ref('stock.model_stock_lot').id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': summary,
                    'note': note,
                    'user_id': user.id,
                    'date_deadline': today,
                })
        
        _logger.info(f"Created expiry alerts for {len(lots_warning)} lots")

    @api.model
    def cron_low_stock_alert(self):
        """
        Daily Cron (02:00): Check for low stock products
        """
        _logger.info("Starting low stock alert cron job...")
        
        # Find drug products with low stock
        low_stock_products = self.env['product.product'].search([
            ('is_drug', '=', True),
            ('qty_available', '<=', 'min_qty'),
            ('min_qty', '>', 0),
        ])
        
        if not low_stock_products:
            _logger.info("No low stock products found")
            return
        
        # Get stock manager users
        stock_group = self.env.ref('pharmacy_core.group_pharmacy_stock')
        stock_users = stock_group.users
        
        today = date.today()
        
        for product in low_stock_products:
            summary = f"Low Stock: {product.name}"
            note = f"""
                <p><strong>📦 LOW STOCK ALERT</strong></p>
                <ul>
                    <li>Product: {product.name}</li>
                    <li>Current Stock: {product.qty_available}</li>
                    <li>Minimum Required: {product.min_qty}</li>
                </ul>
                <p><strong>Action Required:</strong> Create purchase order to replenish stock.</p>
            """
            
            for user in stock_users:
                self.env['mail.activity'].create({
                    'res_id': product.id,
                    'res_model_id': self.env.ref('product.model_product_product').id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': summary,
                    'note': note,
                    'user_id': user.id,
                    'date_deadline': today,
                })
        
        _logger.info(f"Created low stock alerts for {len(low_stock_products)} products")

    @api.model
    def cron_dead_stock_detection(self):
        """
        Monthly Cron: Detect dead stock (no sales in X days)
        Default threshold: 180 days
        """
        _logger.info("Starting dead stock detection cron job...")
        
        threshold_days = 180
        threshold_date = date.today() - timedelta(days=threshold_days)
        
        # Get all drug products
        drug_products = self.env['product.product'].search([
            ('is_drug', '=', True),
            ('qty_available', '>', 0),
        ])
        
        dead_stock_products = []
        
        for product in drug_products:
            # Check last sale date
            last_sale = self.env['sale.order.line'].search([
                ('product_id', '=', product.id),
                ('order_id.state', 'in', ['sale', 'done']),
                ('order_id.date_order', '>=', threshold_date),
            ], limit=1)
            
            # Also check POS sales
            last_pos_sale = self.env['pos.order.line'].search([
                ('product_id', '=', product.id),
                ('order_id.state', 'in', ['paid', 'done', 'invoiced']),
                ('order_id.date_order', '>=', threshold_date),
            ], limit=1)
            
            if not last_sale and not last_pos_sale:
                dead_stock_products.append(product)
        
        if not dead_stock_products:
            _logger.info("No dead stock detected")
            return
        
        # Get pharmacy admin users
        admin_group = self.env.ref('pharmacy_core.group_pharmacy_admin')
        admin_users = admin_group.users
        
        today = date.today()
        
        for product in dead_stock_products:
            summary = f"Dead Stock: {product.name} (No sales in {threshold_days} days)"
            note = f"""
                <p><strong>⚠️ DEAD STOCK DETECTED</strong></p>
                <ul>
                    <li>Product: {product.name}</li>
                    <li>Current Stock: {product.qty_available}</li>
                    <li>No Sales Since: {threshold_date}</li>
                    <li>Days Threshold: {threshold_days}</li>
                </ul>
                <p><strong>Action Required:</strong> Consider promotion, discount, or return to supplier.</p>
            """
            
            for user in admin_users:
                self.env['mail.activity'].create({
                    'res_id': product.id,
                    'res_model_id': self.env.ref('product.model_product_product').id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': summary,
                    'note': note,
                    'user_id': user.id,
                    'date_deadline': today,
                })
        
        _logger.info(f"Created dead stock alerts for {len(dead_stock_products)} products")
