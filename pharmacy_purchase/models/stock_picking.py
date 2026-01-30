# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    """Stock Picking Extension for Pharmacy Purchase
    
    Enforces lot and expiry date requirements on receipt.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'stock.picking'

    @api.constrains('state')
    def _check_drug_lot_expiry_on_validate(self):
        """
        CRITICAL: Block validation if drug products missing lot or expiry
        """
        for picking in self:
            if picking.state == 'done' and picking.picking_type_code == 'incoming':
                for move_line in picking.move_line_ids:
                    if move_line.product_id.is_drug:
                        # Check lot is assigned
                        if not move_line.lot_id:
                            raise ValidationError(
                                f'Cannot validate receipt!\n\n'
                                f'Product: {move_line.product_id.name}\n'
                                f'Missing: Lot Number\n\n'
                                f'All pharmaceutical products require lot tracking.'
                            )
                        
                        # Check expiry date is set
                        if not move_line.lot_id.expiration_date:
                            raise ValidationError(
                                f'Cannot validate receipt!\n\n'
                                f'Product: {move_line.product_id.name}\n'
                                f'Lot: {move_line.lot_id.name}\n'
                                f'Missing: Expiration Date\n\n'
                                f'All pharmaceutical lots require an expiration date.'
                            )

    def button_validate(self):
        """Override validation to check drug requirements before processing"""
        # Pre-check for better UX (before actual validation)
        for picking in self:
            if picking.picking_type_code == 'incoming':
                for move_line in picking.move_line_ids:
                    if move_line.product_id.is_drug and move_line.quantity > 0:
                        if not move_line.lot_id:
                            raise ValidationError(
                                f'Lot number required for: {move_line.product_id.name}'
                            )
        
        return super(StockPicking, self).button_validate()
