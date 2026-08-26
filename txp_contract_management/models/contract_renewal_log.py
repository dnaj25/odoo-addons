from odoo import models, fields, api

class ContractRenewalLog(models.Model):
    _name = 'contract.renewal.log'
    _description = 'Contract Renewal History'
    _order = 'renewal_date desc, id desc'

    name = fields.Char(string='Reference', compute='_compute_name', store=True)
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

    @api.depends('contract_id.name', 'renewal_date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"Renewal - {rec.contract_id.name or ''}"