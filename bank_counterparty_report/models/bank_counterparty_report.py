from odoo import models, fields, api, tools

class BankCounterpartyReport(models.Model):
    _name = 'bank.counterparty.report'
    _description = 'Bank Counterparty Report'
    _auto = False
    _rec_name = 'move_id'
    _order = 'date desc, id desc'

    date = fields.Date(string='Date', readonly=True)
    move_id = fields.Many2one('account.move', string='Journal Entry', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
    bank_account_id = fields.Many2one('account.account', string='Bank Account', readonly=True)
    counterparty_account_id = fields.Many2one('account.account', string='Counterparty Account', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    amount = fields.Float(string='Amount', readonly=True)
    type = fields.Selection([
        ('incoming', 'Incoming (الوارد)'),
        ('outgoing', 'Outgoing (المنصرف)'),
    ], string='Type', readonly=True)
    payment_ref = fields.Char(string='Payment Reference', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    aml_counter.id AS id,
                    aml_bank.date AS date,
                    aml_bank.move_id AS move_id,
                    m.journal_id AS journal_id,
                    aml_bank.account_id AS bank_account_id,
                    aml_counter.account_id AS counterparty_account_id,
                    aml_counter.partner_id AS partner_id,
                    (aml_counter.credit - aml_counter.debit) AS amount,
                    CASE 
                        WHEN (aml_counter.credit - aml_counter.debit) > 0 THEN 'incoming'
                        ELSE 'outgoing'
                    END AS type,
                    COALESCE(m.payment_reference, aml_bank.name) AS payment_ref
                FROM account_move_line aml_bank
                JOIN account_move m ON m.id = aml_bank.move_id
                JOIN account_journal j ON j.id = m.journal_id
                JOIN account_account acc_bank ON acc_bank.id = aml_bank.account_id
                
                -- Join counterparty lines in same move that are NOT bank accounts
                JOIN account_move_line aml_counter ON aml_counter.move_id = aml_bank.move_id AND aml_counter.id != aml_bank.id
                JOIN account_account acc ON acc.id = aml_counter.account_id
                
                WHERE j.type = 'bank'
                  AND (acc_bank.account_type = 'asset_cash')
                  AND (acc.account_type != 'asset_cash')
            )
        """)
