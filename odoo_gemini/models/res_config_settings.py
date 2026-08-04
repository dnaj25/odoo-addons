from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gemini_api_key = fields.Char(
        string='Gemini API Key',
        config_parameter='odoo_gemini.api_key',
        help="Google Gemini API Key for authentication."
    )
    gemini_model_name = fields.Selection(
        [
            ('gemini-flash-latest', 'Gemini Flash (Recommended / Free Tier)'),
            ('gemini-3.5-flash', 'Gemini 3.5 Flash (Latest Fast)'),
            ('gemini-2.0-flash', 'Gemini 2.0 Flash (Fast & Capable)'),
            ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
            ('gemini-1.5-flash', 'Gemini 1.5 Flash (Deprecated)'),
        ],
        string='Gemini Model Name',
        config_parameter='odoo_gemini.model_name',
        default='gemini-flash-latest',
        help="Select the default Gemini model name for completions."
    )
