# models/contract_type.py
from odoo import models, fields

class ContractType(models.Model):
    _name = 'contract.type'
    _description = 'Contract Category / Type'

    name = fields.Char(string='Type Name', required=True) # مثل: عقود موظفين، إيجار، تراخيص
    code = fields.Char(string='Code')
    color = fields.Integer(string='Color Index')


# models/contract_renewal_log.py
from odoo import models, fields, api

class ContractRenewalLog(models.Model):
    _name = 'contract.renewal.log'
    _description = 'Contract Renewal History'

    contract_id = fields.Many2one('contract.contract', string='Contract', required=True, ondelete='cascade')
    renewal_date = fields.Date(string='Renewal Date', default=fields.Date.today, required=True)
    
    old_start_date = fields.Date(string='Previous Start Date')
    old_end_date = fields.Date(string='Previous End Date')
    old_amount = fields.Monetary(string='Previous Amount', currency_field='currency_id')

    new_start_date = fields.Date(string='New Start Date', required=True)
    new_end_date = fields.Date(string='New End Date', required=True)
    new_amount = fields.Monetary(string='New Amount', currency_field='currency_id', required=True)
    
    currency_id = fields.Many2one('res.currency', related='contract_id.currency_id')
    note = fields.Text(string='Renewal Notes')

    def action_confirm_renewal(self):
        """تحديث بيانات العقد الأصلي وتسجيل العملية"""
        self.contract_id.write({
            'start_date': self.new_start_date,
            'end_date': self.new_end_date,
            'amount': self.new_amount,
            'state': 'active',
        })
        return {'type': 'ir.actions.act_window_close'}