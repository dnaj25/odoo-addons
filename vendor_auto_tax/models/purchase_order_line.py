from odoo import models, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_id', 'product_qty', 'order_id.partner_id')
    def _compute_tax_id(self):
        # First compute standard taxes (e.g. from product settings)
        super()._compute_tax_id()
        # Then, if the vendor has a default purchase tax set, override with it
        for line in self:
            vendor = line.order_id.partner_id
            if vendor and vendor.x_default_purchase_tax_id:
                line.tax_ids = [(6, 0, [vendor.x_default_purchase_tax_id.id])]
