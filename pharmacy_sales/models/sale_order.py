# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """Sale Order Extension for Pharmacy
    
    Tracks pharmaceutical sales and adds validations.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'sale.order'

    has_drug_products = fields.Boolean(
        string='Contains Drugs',
        compute='_compute_has_drug_products',
        store=True
    )
    
    total_profit = fields.Monetary(
        string='Total Profit',
        compute='_compute_total_profit',
        store=True
    )

    @api.depends('order_line.product_id.is_drug')
    def _compute_has_drug_products(self):
        """Check if order contains drugs"""
        for order in self:
            order.has_drug_products = any(line.product_id.is_drug for line in order.order_line)

    @api.depends('order_line.profit_amount')
    def _compute_total_profit(self):
        """Calculate total profit from all lines"""
        for order in self:
            order.total_profit = sum(order.order_line.mapped('profit_amount'))


class SaleOrderLine(models.Model):
    """Sale Order Line Extension for Pharmacy
    
    Adds profit tracking and stock validation for drugs.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'sale.order.line'

    is_drug_line = fields.Boolean(
        string='Is Drug',
        related='product_id.is_drug',
        store=True
    )
    
    cost_price = fields.Float(
        string='Cost Price',
        compute='_compute_cost_price',
        store=True,
        digits='Product Price'
    )
    
    profit_amount = fields.Monetary(
        string='Profit',
        compute='_compute_profit',
        store=True
    )
    
    profit_margin = fields.Float(
        string='Profit Margin %',
        compute='_compute_profit',
        store=True
    )

    @api.depends('product_id', 'product_uom_qty')
    def _compute_cost_price(self):
        """Compute cost price from product standard price"""
        for line in self:
            if line.product_id:
                line.cost_price = line.product_id.standard_price * line.product_uom_qty
            else:
                line.cost_price = 0.0

    @api.depends('price_subtotal', 'cost_price')
    def _compute_profit(self):
        """Calculate profit and margin"""
        for line in self:
            line.profit_amount = line.price_subtotal - line.cost_price
            if line.price_subtotal > 0:
                line.profit_margin = (line.profit_amount / line.price_subtotal) * 100
            else:
                line.profit_margin = 0.0

    @api.constrains('product_uom_qty', 'product_id')
    def _check_stock_availability(self):
        """Block negative stock sales for drugs"""
        for line in self:
            if line.is_drug_line and line.product_uom_qty > 0:
                available_qty = line.product_id.qty_available
                if available_qty < line.product_uom_qty:
                    raise ValidationError(
                        f'Insufficient stock for {line.product_id.name}!\n\n'
                        f'Requested: {line.product_uom_qty}\n'
                        f'Available: {available_qty}\n\n'
                        f'Negative stock sales are not allowed for pharmaceutical products.'
                    )
