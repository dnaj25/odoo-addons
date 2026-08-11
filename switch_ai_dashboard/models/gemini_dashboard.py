# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SwitchAiDashboard(models.AbstractModel):
    _name = 'switch.ai.dashboard'
    _description = 'Switch Fintech AI Dashboard Service'

    @api.model
    def get_dashboard_data(self):
        """
        Fetches business metrics from the database for dashboard display.
        """
        # 1. Sales metrics
        sales_orders = self.env['sale.order'].sudo().search([('state', 'in', ['sale', 'done'])])
        total_sales = sum(sales_orders.mapped('amount_total'))
        sales_count = len(sales_orders)

        # 2. Purchase metrics
        purchase_orders = self.env['purchase.order'].sudo().search([('state', 'in', ['purchase', 'done'])])
        total_purchases = sum(purchase_orders.mapped('amount_total'))
        purchases_count = len(purchase_orders)

        # 3. Invoices & Receivables
        invoices = self.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ])
        total_invoices = sum(invoices.mapped('amount_total'))
        
        unpaid_invoices = sum(invoices.filtered(lambda m: m.payment_state in ['not_paid', 'partial']).mapped('amount_residual'))

        # 4. Customers count
        customer_count = self.env['res.partner'].sudo().search_count([('customer_rank', '>', 0)])

        # 5. Monthly Sales chart data (recent 6 months)
        # For simplicity, let's gather recent sales grouped by month
        recent_sales = []
        try:
            self._cr.execute("""
                SELECT to_char(date_order, 'YYYY-MM') as month, sum(amount_total) as total
                FROM sale_order
                WHERE state IN ('sale', 'done')
                GROUP BY to_char(date_order, 'YYYY-MM')
                ORDER BY month DESC
                LIMIT 6
            """)
            rows = self._cr.fetchall()
            recent_sales = [{'month': r[0], 'total': float(r[1])} for r in reversed(rows)]
        except Exception as e:
            _logger.error("Failed to query monthly sales chart data: %s", e)

        return {
            'total_sales': round(total_sales, 2),
            'sales_count': sales_count,
            'total_purchases': round(total_purchases, 2),
            'purchases_count': purchases_count,
            'total_invoices': round(total_invoices, 2),
            'unpaid_invoices': round(unpaid_invoices, 2),
            'customer_count': customer_count,
            'chart_data': recent_sales,
        }

    @api.model
    def get_ai_insights(self):
        """
        Sends business metrics to Gemini AI and returns structured executive insights in Arabic.
        """
        data = self.get_dashboard_data()
        
        prompt = f"""
        Analyze the following Odoo business statistics for Switch Fintech:
        - Total Sales: {data['total_sales']} SAR (from {data['sales_count']} sales orders)
        - Total Purchases (Procurements): {data['total_purchases']} SAR (from {data['purchases_count']} purchase orders)
        - Total Customer Invoices: {data['total_invoices']} SAR
        - Total Outstanding/Unpaid Invoices: {data['unpaid_invoices']} SAR
        - Total Active Customers: {data['customer_count']}
        
        Write a concise, professional executive business briefing in Arabic.
        Structure the response with:
        1. ملخص الأداء المالي (Brief financial performance summary)
        2. تنبيهات المخاطر (Risk warnings like unpaid invoices ratio)
        3. 3 توصيات ذكية موجهة لزيادة الأرباح وتقليل التكاليف (3 smart recommendations)
        
        Format the response nicely in clean Markdown with bold headers and bullet points. Use brand-appropriate language.
        """
        
        try:
            gemini_service = self.env['gemini.service']
            insights = gemini_service.generate_content(prompt)
            return {
                'status': 'success',
                'insights': insights
            }
        except Exception as e:
            _logger.error("Failed to fetch AI insights: %s", e)
            return {
                'status': 'error',
                'message': str(e)
            }
