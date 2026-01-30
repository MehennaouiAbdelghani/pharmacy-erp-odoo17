# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    """Purchase Order Extension for Pharmacy
    
    Adds drug-specific validations for purchase orders.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'purchase.order'

    has_drug_products = fields.Boolean(
        string='Contains Drugs',
        compute='_compute_has_drug_products',
        store=True
    )
    
    drug_product_count = fields.Integer(
        string='Drug Products',
        compute='_compute_has_drug_products',
        store=True
    )

    @api.depends('order_line.product_id.is_drug')
    def _compute_has_drug_products(self):
        """Check if PO contains any pharmaceutical products"""
        for order in self:
            drug_lines = order.order_line.filtered(lambda l: l.product_id.is_drug)
            order.has_drug_products = bool(drug_lines)
            order.drug_product_count = len(drug_lines)


class PurchaseOrderLine(models.Model):
    """Purchase Order Line Extension
    
    Tracks drug status for purchase order lines.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'purchase.order.line'

    is_drug_line = fields.Boolean(
        string='Is Drug',
        related='product_id.is_drug',
        store=True
    )
