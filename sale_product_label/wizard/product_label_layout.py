# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api

class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    sale_order_ids = fields.Many2many('sale.order', string="Sales Orders")
    sale_quantity = fields.Selection([
        ('sale', 'Ordered Quantities'),
        ('custom', 'Custom')
    ], string="Quantity to print", required=True, default='custom')

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        
        if self.sale_quantity == 'sale' and self.sale_order_ids:
            quantities = defaultdict(int)
            for order in self.sale_order_ids:
                for line in order.order_line:
                    if line.product_id and not line.display_type and line.product_id.type in ('consu', 'product'):
                        qty = int(line.product_uom_qty)
                        if qty > 0:
                            quantities[line.product_id.id] += qty
            # Update the quantities in the data dictionary passed to the report
            data['quantity_by_product'] = {p: q for p, q in quantities.items() if q > 0}
            
        return xml_id, data
