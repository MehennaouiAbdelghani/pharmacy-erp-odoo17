# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PharmacyDrugCategory(models.Model):
    """Drug Category Management Model
    
    Manages pharmaceutical product categories with hierarchical structure.
    Optimized for fast lookups and category-based filtering.
    
    Author: Abdelghani Mehennaoui
    """
    _name = 'pharmacy.drug.category'
    _description = 'Pharmacy Drug Category'
    _order = 'name'
    _parent_store = True
    _rec_name = 'complete_name'

    name = fields.Char(
        string='Category Name',
        required=True,
        translate=True,
        index=True,
        help='Name of the drug category'
    )
    
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        recursive=True,
        store=True,
        index=True
    )
    
    parent_id = fields.Many2one(
        'pharmacy.drug.category',
        string='Parent Category',
        index=True,
        ondelete='cascade',
        help='Parent category for hierarchical classification'
    )
    
    parent_path = fields.Char(
        index=True,
        unaccent=False
    )
    
    child_ids = fields.One2many(
        'pharmacy.drug.category',
        'parent_id',
        string='Child Categories'
    )
    
    product_count = fields.Integer(
        string='Number of Products',
        compute='_compute_product_count'
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    active = fields.Boolean(
        default=True,
        help='Set to false to hide this category without deleting it'
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name, parent_id)', 
         'A category with the same name already exists at this level!')
    ]

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """Compute complete hierarchical name"""
        for category in self:
            if category.parent_id:
                category.complete_name = f'{category.parent_id.complete_name} / {category.name}'
            else:
                category.complete_name = category.name

    def _compute_product_count(self):
        """Compute number of products in this category"""
        for category in self:
            category.product_count = self.env['product.template'].search_count([
                ('pharmacy_category_id', '=', category.id)
            ])

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        """Prevent recursive parent relationships"""
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')
