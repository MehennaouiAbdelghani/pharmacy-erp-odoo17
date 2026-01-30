# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    """Product Template Extension for FIFO Enforcement
    
    Forces FIFO removal strategy on all pharmaceutical products.
    This ensures oldest stock (nearest expiry) is used first.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-set FIFO strategy for drugs on creation"""
        # Get FIFO removal strategy
        fifo_strategy = self.env.ref('stock.removal_fifo', raise_if_not_found=False)
        
        for vals in vals_list:
            if vals.get('is_drug') and fifo_strategy:
                vals['categ_id'] = vals.get('categ_id') or self.env.ref('product.product_category_all').id
                
        products = super(ProductTemplate, self).create(vals_list)
        
        # Force FIFO after creation for drug products
        if fifo_strategy:
            for product in products:
                if product.is_drug:
                    # Set FIFO on product category if not already set
                    if product.categ_id and product.categ_id.removal_strategy_id != fifo_strategy:
                        product.categ_id.removal_strategy_id = fifo_strategy.id
        
        return products

    def write(self, vals):
        """Maintain FIFO strategy on updates"""
        result = super(ProductTemplate, self).write(vals)
        
        # If marking as drug, ensure FIFO
        if vals.get('is_drug'):
            fifo_strategy = self.env.ref('stock.removal_fifo', raise_if_not_found=False)
            if fifo_strategy:
                for product in self:
                    if product.categ_id and product.categ_id.removal_strategy_id != fifo_strategy:
                        product.categ_id.removal_strategy_id = fifo_strategy.id
        
        return result


class ProductCategory(models.Model):
    """Product Category Extension
    
    Prevents removal strategy override for drug categories
    """
    _inherit = 'product.category'

    def write(self, vals):
        """Block FIFO removal strategy change for categories with drugs"""
        from odoo.exceptions import ValidationError
        
        if 'removal_strategy_id' in vals:
            fifo_strategy = self.env.ref('stock.removal_fifo', raise_if_not_found=False)
            if fifo_strategy:
                for category in self:
                    # Check if category has drug products
                    drug_count = self.env['product.template'].search_count([
                        ('categ_id', '=', category.id),
                        ('is_drug', '=', True)
                    ])
                    
                    if drug_count > 0 and vals['removal_strategy_id'] != fifo_strategy.id:
                        raise ValidationError(
                            f'Cannot change removal strategy for category "{category.name}"!\n'
                            f'This category contains {drug_count} pharmaceutical product(s).\n'
                            f'FIFO strategy is mandatory for all pharmaceutical products.'
                        )
        
        return super(ProductCategory, self).write(vals)
