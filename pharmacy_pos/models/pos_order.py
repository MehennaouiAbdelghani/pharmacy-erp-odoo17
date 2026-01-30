# -*- coding: utf-8 -*-

from odoo import models, fields


class PosOrder(models.Model):
    """POS Order Extension for Pharmacy
    
    Applies same rules as sale orders for pharmacy products.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'pos.order'

    has_drug_products = fields.Boolean(
        string='Contains Drugs',
        compute='_compute_has_drug_products'
    )

    def _compute_has_drug_products(self):
        """Check if POS order contains drugs"""
        for order in self:
            order.has_drug_products = any(line.product_id.is_drug for line in order.lines)

    def _prepare_stock_move_vals(self, line):
        """Override to ensure FIFO lot selection for drugs"""
        vals = super(PosOrder, self)._prepare_stock_move_vals(line)
        
        # The stock move will trigger auto-lot assignment from pharmacy_sales module
        # No additional logic needed here as it inherits from pharmacy_sales
        
        return vals


class PosOrderLine(models.Model):
    """POS Order Line Extension
    
    Tracks drug products in POS.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'pos.order.line'

    is_drug_line = fields.Boolean(
        string='Is Drug',
        related='product_id.is_drug'
    )
