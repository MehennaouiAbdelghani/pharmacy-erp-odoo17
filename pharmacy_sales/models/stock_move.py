# -*- coding: utf-8 -*-

from odoo import models, api


class StockMove(models.Model):
    """Stock Move Extension for Pharmacy Sales
    
    Implements automatic FIFO lot selection for drug sales.
    Ensures nearest expiry lots are sold first.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'stock.move'

    def _action_assign(self):
        """Override to auto-assign lot with nearest expiry (FIFO)"""
        result = super(StockMove, self)._action_assign()
        
        # Auto-assign lots for drug products
        for move in self:
            if move.product_id.is_drug and move.product_id.tracking == 'lot':
                self._auto_assign_drug_lot(move)
        
        return result

    def _auto_assign_drug_lot(self, move):
        """
        Auto-assign lot with nearest expiry date (FIFO logic)
        Performance optimized: Single query with ORDER BY
        """
        if not move.move_line_ids:
            return
        
        for move_line in move.move_line_ids:
            if not move_line.lot_id and move_line.quantity > 0:
                # Find available lot with nearest expiry
                available_lot = self.env['stock.lot'].search([
                    ('product_id', '=', move.product_id.id),
                    ('expiration_date', '!=', False),
                    ('expired', '=', False),
                ], order='expiration_date asc', limit=1)
                
                if available_lot:
                    move_line.lot_id = available_lot.id


class StockMoveLine(models.Model):
    """Stock Move Line Extension for Sales
    
    Additional validation for outgoing moves.
    
    Author: Abdelghani Mehennaoui
    """
    _inherit = 'stock.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure lot assignment for drug outgoing moves"""
        lines = super(StockMoveLine, self).create(vals_list)
        
        for line in lines:
            # Auto-assign lot for outgoing drug moves without lot
            if (line.picking_code == 'outgoing' and 
                line.product_id.is_drug and 
                not line.lot_id and 
                line.quantity > 0):
                
                # Find nearest expiry lot
                available_lot = self.env['stock.lot'].search([
                    ('product_id', '=', line.product_id.id),
                    ('expiration_date', '!=', False),
                    ('expired', '=', False),
                ], order='expiration_date asc', limit=1)
                
                if available_lot:
                    line.lot_id = available_lot.id
        
        return lines
