# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class StockMoveLine(models.Model):
    """Stock Move Line Extension for Pharmacy
    
    Enforces expiry date validation and blocks moves of expired lots.
    Critical for pharmaceutical compliance and patient safety.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'stock.move.line'

    lot_expiration_date = fields.Datetime(
        string='Lot Expiry Date',
        related='lot_id.expiration_date',
        store=True,
        readonly=True
    )
    
    is_expired = fields.Boolean(
        string='Lot Expired',
        related='lot_id.expired',
        store=True,
        readonly=True
    )
    
    is_drug_move = fields.Boolean(
        string='Is Drug Move',
        related='product_id.is_drug',
        store=True,
        index=True
    )

    @api.constrains('lot_id', 'quantity', 'product_id')
    def _check_expired_lot(self):
        """
        CRITICAL CONSTRAINT: Block any move with expired lot
        This is mandatory for pharmaceutical compliance
        """
        today = date.today()
        for move_line in self:
            if move_line.is_drug_move and move_line.lot_id:
                if move_line.lot_id.expiration_date:
                    expiry = fields.Date.from_string(move_line.lot_id.expiration_date)
                    if expiry < today:
                        raise ValidationError(
                            f'Cannot process move for EXPIRED lot!\n\n'
                            f'Product: {move_line.product_id.name}\n'
                            f'Lot: {move_line.lot_id.name}\n'
                            f'Expiry Date: {move_line.lot_id.expiration_date}\n\n'
                            f'Expired lots cannot be sold or transferred.'
                        )

    @api.constrains('lot_id')
    def _check_lot_required_for_drugs(self):
        """Ensure lot is set for all drug movements"""
        for move_line in self:
            if move_line.is_drug_move and move_line.quantity > 0 and not move_line.lot_id:
                raise ValidationError(
                    f'Lot number is mandatory for pharmaceutical product: {move_line.product_id.name}'
                )

    def write(self, vals):
        """Override write to maintain expiry constraints"""
        result = super(StockMoveLine, self).write(vals)
        # Re-check expiry if lot or quantity changed
        if 'lot_id' in vals or 'quantity' in vals:
            self._check_expired_lot()
        return result

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to enforce expiry checking"""
        lines = super(StockMoveLine, self).create(vals_list)
        lines._check_expired_lot()
        lines._check_lot_required_for_drugs()
        return lines
