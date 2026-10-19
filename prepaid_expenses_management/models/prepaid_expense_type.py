# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PrepaidExpenseType(models.Model):
    _name = 'prepaid.expense.type'
    _description = 'Prepaid Expense Category / Type'
    _order = 'sequence, name'

    name = fields.Char(string='Category Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    code = fields.Char(string='Code', size=16)
    active = fields.Boolean(string='Active', default=True)
    
    prepaid_account_id = fields.Many2one(
        'account.account',
        string='Default Prepaid Asset Account',
        help='Default asset balance sheet account (e.g., Prepaid Rent / Prepaid Expenses)'
    )
    expense_account_id = fields.Many2one(
        'account.account',
        string='Default Expense Account',
        help='Default P&L expense account (e.g., Rent Expense, Insurance Expense)'
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Default Recognition Journal',
        domain="[('type', 'in', ['general', 'purchase'])]",
        help='Default journal to create periodic deduction entries'
    )
    default_periodicity = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly (3 Months)'),
        ('semi_annually', 'Semi-Annually (6 Months)'),
        ('annually', 'Annually'),
        ('custom', 'Custom Periods'),
    ], string='Default Frequency', default='monthly')
    
    reminder_days_before = fields.Integer(
        string='Default Renewal Notice (Days)',
        default=30,
        help='Number of days before expiration to alert the user for renewal (e.g., 30 for 1 month before)'
    )
    description = fields.Text(string='Notes / Description')
    
    expense_count = fields.Integer(
        string='Expenses Count',
        compute='_compute_expense_count'
    )

    def _compute_expense_count(self):
        for rec in self:
            rec.expense_count = self.env['prepaid.expense'].search_count([('category_id', '=', rec.id)])

    def action_view_expenses(self):
        self.ensure_one()
        return {
            'name': _('Prepaid Expenses: %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'prepaid.expense',
            'view_mode': 'list,kanban,form,graph,pivot',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
