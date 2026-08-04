import sys
sys.path.append(r"C:\Users\Start\AppData\Roaming\Python\Python312\site-packages")
try:
    import markdown
except ImportError:
    markdown = None

from markupsafe import Markup
from odoo import fields, models, api

class GeminiChatWizard(models.TransientModel):
    _name = 'gemini.chat.wizard'
    _description = 'Gemini AI Assistant'

    prompt = fields.Text(string='Ask Gemini', required=True)
    response = fields.Html(string='Chat History', readonly=True)

    def action_send(self):
        self.ensure_one()
        # Instruct Gemini to format list data as markdown tables
        enhanced_prompt = (
            f"{self.prompt}\n\n"
            "Note: Please format any list, product list, tax list, or tabular comparisons "
            "as a standard Markdown Table for clarity."
        )
        
        # Call the Gemini service helper
        ai_response = self.env['gemini.service'].generate_content(enhanced_prompt)
        
        # Convert markdown formatting to HTML (with table support)
        if markdown:
            formatted_response = markdown.markdown(ai_response, extensions=['tables'])
            # Add native bootstrap styling to tables
            formatted_response = formatted_response.replace('<table>', '<table class="table table-striped table-bordered mt-2 mb-2">')
        else:
            formatted_response = ai_response.replace('\n', '<br/>')
        
        # Format the chat entry using Markup to prevent escaping
        new_entry = Markup(
            f"<div style='margin-bottom:8px; color: #1f2937;'><b>User:</b> {self.prompt}</div>"
            f"<div style='margin-bottom:16px; background-color:#f3f4f6; padding:12px; border-radius:6px; color: #111827;'><b>Gemini:</b> {formatted_response}</div>"
        )
        
        # Append to history safely preserving HTML rendering
        if self.response:
            self.response = Markup(self.response) + new_entry
        else:
            self.response = new_entry
            
        # Clear prompt for next input
        self.prompt = ""
        
        # Keep wizard popup open
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }
