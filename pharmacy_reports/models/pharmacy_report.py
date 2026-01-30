# --- coding: utf-8 -*-

from odoo import models, fields, api


class PharmacyReport(models.Model):
    """Pharmacy Reporting Base Model
    
    Provides data aggregation for pharmacy reports.
    
    Author: Abdelghani Mehennaoui
    """
    _name = 'pharmacy.report'
    _description = 'Pharmacy Report'
    _auto = False
    _order = 'product_id, date desc'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    quantity = fields.Float(string='Quantity', readonly=True)
    amount = fields.Float(string='Amount', readonly=True)
    profit = fields.Float(string='Profit', readonly=True)
    
    def init(self):
        """Create SQL view for reporting"""
        from odoo import tools
        tools.drop_view_if_exists(self.env.cr, self._table)
        
        query = """
            CREATE OR REPLACE VIEW pharmacy_report AS (
                SELECT
                    row_number() OVER () AS id,
                    sol.product_id,
                    so.date_order::date AS date,
                    SUM(sol.product_uom_qty) AS quantity,
                    SUM(sol.price_subtotal) AS amount,
                    SUM(sol.profit_amount) AS profit
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                JOIN product_product pp ON sol.product_id = pp.id
                JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE pt.is_drug = true
                  AND so.state IN ('sale', 'done')
                GROUP BY sol.product_id, so.date_order::date
            )
        """
        self.env.cr.execute(query)
