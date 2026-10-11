# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PrepaidExpenseLine(models.Model):
    _name = 'prepaid.expense.line'
    _description = 'Prepaid Expense Recognition Line / Installment'
    _order = 'date asc, sequence asc'

    expense_id = fields.Many2one(
        'prepaid.expense',
        string='Prepaid Contract',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(string='#', default=1)
    name = fields.Char(string='Description', required=True)
    date = fields.Date(string='Recognition Date', required=True)
    amount = fields.Monetary(
        string='Amount to Recognize',
        required=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='expense_id.currency_id',
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='expense_id.company_id',
        store=True,
        readonly=True
    )
    move_id = fields.Many2one(
        'account.move',
        string='Journal Entry',
        readonly=True,
        copy=False
    )
    state = fields.Selection([
        ('draft', 'Scheduled'),
        ('posted', 'Recognized / Posted'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True)

    def action_post_entry(self):
        self.ensure_one()
        if self.state == 'posted':
            raise UserError(_('This installment has already been recognized and posted.'))
        if self.amount <= 0:
            raise UserError(_('Installment amount must be greater than zero.'))

        exp = self.expense_id
        move_vals = {
            'journal_id': exp.journal_id.id,
            'date': self.date,
            'ref': f"{exp.name} - {exp.title} (Period {self.sequence}/{exp.lines_count})",
            'move_type': 'entry',
            'company_id': exp.company_id.id,
            'line_ids': [
                # Debit Expense Account (P&L)
                (0, 0, {
                    'name': f"{exp.title} - Recognition ({self.sequence}/{exp.lines_count})",
                    'account_id': exp.expense_account_id.id,
                    'partner_id': exp.partner_id.id if exp.partner_id else False,
                    'debit': self.amount,
                    'credit': 0.0,
                    'analytic_distribution': exp.analytic_distribution if exp.analytic_distribution else False,
                }),
                # Credit Prepaid Asset Account (Balance Sheet)
                (0, 0, {
                    'name': f"{exp.title} - Prepaid Offset ({self.sequence}/{exp.lines_count})",
                    'account_id': exp.prepaid_account_id.id,
                    'partner_id': exp.partner_id.id if exp.partner_id else False,
                    'debit': 0.0,
                    'credit': self.amount,
                }),
            ],
        }

        move = self.env['account.move'].create(move_vals)
        move.action_post()
        
        self.write({
            'move_id': move.id,
            'state': 'posted',
        })
        return True

    def action_view_move(self):
        self.ensure_one()
        if not self.move_id:
            raise UserError(_('No journal entry linked to this installment.'))
        return {
            'name': _('Journal Entry: %s') % self.move_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
