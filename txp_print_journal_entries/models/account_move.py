from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_total_debit(self):
        """حساب إجمالي المدين للقيد"""
        self.ensure_one()
        return sum(line.debit for line in self.line_ids)

    def get_total_credit(self):
        """حساب إجمالي الدائن للقيد"""
        self.ensure_one()
        return sum(line.credit for line in self.line_ids)