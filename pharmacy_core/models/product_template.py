# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    """Product Template Extension for Pharmacy
    
    Extends product.template with pharmacy-specific fields and constraints.
    Implements strict validation for pharmacy products.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'product.template'

    is_drug = fields.Boolean(
        string='Is a Drug',
        default=False,
        index=True,
        help='Check this if the product is a pharmaceutical drug'
    )
    
    drug_type = fields.Selection([
        ('otc', 'Over The Counter (OTC)'),
        ('prescription', 'Prescription Required'),
        ('narcotic', 'Narcotic/Controlled Substance')
    ],
        string='Drug Type',
        help='Classification of the drug based on dispensing requirements'
    )
    
    scientific_name = fields.Char(
        string='Scientific Name',
        translate=True,
        index=True,
        help='Scientific/generic name of the drug (e.g., Paracetamol)'
    )
    
    pharmacy_category_id = fields.Many2one(
        'pharmacy.drug.category',
        string='Pharmacy Category',
        index=True,
        ondelete='restrict',
        help='Pharmaceutical category of the product'
    )
    
    min_qty = fields.Float(
        string='Minimum Stock Quantity',
        default=0.0,
        digits='Product Unit of Measure',
        help='Minimum quantity threshold for low stock alerts'
    )

    @api.constrains('is_drug', 'drug_type', 'tracking')
    def _check_drug_constraints(self):
        """Enforce mandatory fields and lot tracking for drugs"""
        for product in self:
            if product.is_drug:
                if not product.drug_type:
                    raise ValidationError(
                        'Drug Type is mandatory for pharmaceutical products!'
                    )
                # Force lot tracking for all drugs (required for expiry management)
                if product.tracking != 'lot':
                    raise ValidationError(
                        'All pharmaceutical products must use Lot/Serial Number tracking for expiry management!'
                    )

    @api.onchange('is_drug')
    def _onchange_is_drug(self):
        """Auto-set tracking when marking as drug"""
        if self.is_drug and self.tracking != 'lot':
            self.tracking = 'lot'

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to enforce drug tracking"""
        for vals in vals_list:
            if vals.get('is_drug'):
                # Force lot tracking for drugs
                vals['tracking'] = 'lot'
                # Ensure drug_type is set
                if not vals.get('drug_type'):
                    raise ValidationError(
                        'Drug Type is mandatory when creating a pharmaceutical product!'
                    )
        return super(ProductTemplate, self).create(vals_list)

    def write(self, vals):
        """Override write to maintain drug constraints"""
        # Prevent removing tracking from drugs
        if 'tracking' in vals and vals['tracking'] != 'lot':
            if any(product.is_drug for product in self):
                raise ValidationError(
                    'Cannot disable lot tracking for pharmaceutical products!'
                )
        return super(ProductTemplate, self).write(vals)
