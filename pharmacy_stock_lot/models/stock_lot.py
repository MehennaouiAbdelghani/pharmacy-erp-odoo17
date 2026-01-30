# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta


class StockLot(models.Model):
    """Stock Lot Extension for Pharmacy
    
    Adds expiry tracking and alert management for pharmaceutical lots.
    Implements automatic expiry detection and threshold-based alerts.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'stock.lot'

    alert_threshold_days = fields.Integer(
        string='Alert Threshold (Days)',
        default=180,
        help='Number of days before expiry to trigger alert. Default: 180 days (6 months)'
    )
    
    expired = fields.Boolean(
        string='Expired',
        compute='_compute_expired',
        store=True,
        index=True,
        help='Automatically computed: True if expiration date has passed'
    )
    
    days_until_expiry = fields.Integer(
        string='Days Until Expiry',
        compute='_compute_days_until_expiry',
        help='Number of days remaining until expiration'
    )
    
    alert_status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'Near Expiry'),
        ('expired', 'Expired')
    ],
        string='Alert Status',
        compute='_compute_alert_status',
        store=True,
        help='Status based on expiry date and alert threshold'
    )
    
    is_drug_lot = fields.Boolean(
        string='Is Drug Lot',
        related='product_id.is_drug',
        store=True,
        index=True
    )

    @api.depends('expiration_date')
    def _compute_expired(self):
        """Compute if lot is expired based on expiration date"""
        today = date.today()
        for lot in self:
            if lot.expiration_date:
                lot.expired = lot.expiration_date.date() < today
            else:
                lot.expired = False

    @api.depends('expiration_date')
    def _compute_days_until_expiry(self):
        """Compute days remaining until expiration"""
        today = date.today()
        for lot in self:
            if lot.expiration_date:
                expiry = lot.expiration_date.date()
                delta = expiry - today
                lot.days_until_expiry = delta.days
            else:
                lot.days_until_expiry = 0

    @api.depends('expiration_date', 'alert_threshold_days', 'expired')
    def _compute_alert_status(self):
        """Compute alert status based on expiry and threshold"""
        today = date.today()
        for lot in self:
            if not lot.expiration_date:
                lot.alert_status = 'ok'
            elif lot.expired:
                lot.alert_status = 'expired'
            else:
                expiry = lot.expiration_date.date()
                threshold_date = today + timedelta(days=lot.alert_threshold_days)
                if expiry <= threshold_date:
                    lot.alert_status = 'warning'
                else:
                    lot.alert_status = 'ok'

    @api.constrains('expiration_date')
    def _check_expiration_date_drug(self):
        """Ensure expiration date is set for drug lots"""
        from odoo.exceptions import ValidationError
        for lot in self:
            if lot.is_drug_lot and not lot.expiration_date:
                raise ValidationError(
                    f'Expiration date is mandatory for pharmaceutical lot {lot.name}!'
                )

    def action_view_stock_moves(self):
        """View all stock moves for this lot"""
        self.ensure_one()
        action = self.env.ref('stock.stock_move_line_action').read()[0]
        action['domain'] = [('lot_id', '=', self.id)]
        action['context'] = {'default_lot_id': self.id}
        return action
