from odoo import models, fields, api, _

class ContractRenewalWizard(models.TransientModel):
    _name = 'contract.renewal.wizard'
    _description = 'Contract Renewal Wizard'

    contract_id = fields.Many2one('contract.contract', string='Contract', required=True, ondelete='cascade')
    
    old_start_date = fields.Date(string='Previous Start Date', readonly=True)
    old_end_date = fields.Date(string='Previous End Date', readonly=True)
    old_amount = fields.Monetary(string='Previous Amount', currency_field='currency_id', readonly=True)

    new_start_date = fields.Date(string='New Start Date', required=True)
    new_end_date = fields.Date(string='New End Date', required=True)
    new_amount = fields.Monetary(string='New Amount', currency_field='currency_id', required=True)
    
    currency_id = fields.Many2one('res.currency', related='contract_id.currency_id')
    note = fields.Text(string='Renewal Notes')

    def action_confirm_renewal(self):
        self.ensure_one()
        # 1. Create history log entry
        self.env['contract.renewal.log'].create({
            'contract_id': self.contract_id.id,
            'old_start_date': self.old_start_date,
            'old_end_date': self.old_end_date,
            'old_amount': self.old_amount,
            'new_start_date': self.new_start_date,
            'new_end_date': self.new_end_date,
            'new_amount': self.new_amount,
            'note': self.note,
        })
        # 2. Update contract record
        self.contract_id.write({
            'start_date': self.new_start_date,
            'end_date': self.new_end_date,
            'amount': self.new_amount,
            'state': 'active',
        })
        return {'type': 'ir.actions.act_window_close'}
