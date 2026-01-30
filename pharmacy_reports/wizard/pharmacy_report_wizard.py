# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PharmacyReportWizard(models.TransientModel):
    """Report Generation Wizard
    
    Allows date range selection for pharmacy reports.
    
    Author: Abdelghani Mehennaoui
    """
    _name = 'pharmacy.report.wizard'
    _description = 'Pharmacy Report Wizard'

    date_from = fields.Date(
        string='Date From',
        required=True,
        default=fields.Date.context_today
    )
    
    date_to = fields.Date(
        string='Date To',
        required=True,
        default=fields.Date.context_today
    )
    
    report_type = fields.Selection([
        ('expired_loss', 'Expired Drugs Loss'),
        ('profit', 'Profit per Product'),
        ('stock_valuation', 'Stock Valuation'),
    ],
        string='Report Type',
        required=True,
        default='profit'
    )

    def action_print_report(self):
        """Generate selected report"""
        self.ensure_one()
        
        if self.report_type == 'expired_loss':
            return self.env.ref('pharmacy_reports.action_report_expired_loss').report_action(self)
        elif self.report_type == 'profit':
            return self.env.ref('pharmacy_reports.action_report_profit').report_action(self)
        elif self.report_type == 'stock_valuation':
            # Use standard stock valuation
            action = self.env.ref('stock.stock_valuation_layer_action').read()[0]
            action['domain'] = [
                ('create_date', '>=', self.date_from),
                ('create_date', '<=', self.date_to),
            ]
            return action

    def _get_expired_lots(self):
        """Get expired lots in date range"""
        return self.env['stock.lot'].search([
            ('is_drug_lot', '=', True),
            ('expired', '=', True),
            ('expiration_date', '>=', self.date_from),
            ('expiration_date', '<=', self.date_to),
        ])

    def _get_profit_data(self):
        """Get profit data grouped by product"""
        query = """
            SELECT 
                pp.id as product_id,
                pt.name->>'en_US' as product_name,
                SUM(sol.product_uom_qty) as qty_sold,
                SUM(sol.price_subtotal) as revenue,
                SUM(sol.cost_price) as cost,
                SUM(sol.profit_amount) as profit
            FROM sale_order_line sol
            JOIN sale_order so ON sol.order_id = so.id
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            WHERE pt.is_drug = true
              AND so.state IN ('sale', 'done')
              AND so.date_order::date >= %s
              AND so.date_order::date <= %s
            GROUP BY pp.id, pt.name
            ORDER BY profit DESC
        """
        
        self.env.cr.execute(query, (self.date_from, self.date_to))
        return self.env.cr.dictfetchall()
