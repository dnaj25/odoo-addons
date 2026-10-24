# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    # Layout & Card Style
    login_layout_style = fields.Selection([
        ('split_left', 'Split Screen (Banner Left / Login Right)'),
        ('split_right', 'Split Screen (Login Left / Banner Right)'),
        ('centered', 'Centered Card (Fullscreen Background)'),
    ], string='Login Layout Style', default='split_left', required=True)

    login_card_theme = fields.Selection([
        ('light', 'Clean Light Card (White)'),
        ('dark', 'Modern Dark Card (#151525)'),
        ('glass', 'Frosted Glassmorphism Card'),
    ], string='Login Card Style', default='light', required=True)

    # Logo Settings
    login_show_logo = fields.Boolean(string='Show Logo on Login Card', default=True)
    login_custom_logo = fields.Binary(
        string='Custom Login Logo',
        attachment=False,
        help='Upload a custom logo for the login screen. If empty, the default Company Logo is used.'
    )

    # Background & Color Settings
    login_bg_type = fields.Selection([
        ('image', 'Background Image (Custom or Default)'),
        ('gradient', 'Custom Two-Color Gradient'),
        ('solid', 'Solid Color Background'),
    ], string='Background Type', default='image', required=True)

    login_bg_image = fields.Binary(
        string='Custom Background Image',
        attachment=False,
        help='Upload any background image for the login page. If empty, the built-in theme background is used.'
    )
    login_bg_color_1 = fields.Char(
        string='Background Color 1',
        default='#2e1a47',
        help='Primary background or gradient start color'
    )
    login_bg_color_2 = fields.Char(
        string='Background Color 2 (Gradient)',
        default='#7239ea',
        help='Gradient end color'
    )
    login_overlay_opacity = fields.Selection([
        ('0.0', 'None (0%)'),
        ('0.3', 'Light (30%)'),
        ('0.6', 'Medium (60%)'),
        ('0.8', 'Dark (80%)'),
    ], string='Background Overlay Darkness', default='0.6', required=True)

    login_primary_color = fields.Char(
        string='Primary Button & Accent Color',
        default='#7239ea',
        help='Main color for the Sign In button, focus rings, and links'
    )

    # Custom Texts
    login_welcome_subtitle = fields.Char(
        string='Welcome Subtitle',
        default='Welcome to',
        translate=True
    )
    login_hero_title = fields.Char(
        string='Main Hero Title',
        translate=True,
        help='Leave empty to automatically display your Company Name'
    )
    login_hero_tagline = fields.Text(
        string='Welcome Tagline / Description',
        default='Sign in to access your business platform.',
        translate=True
    )

    # Footer Settings
    login_show_footer = fields.Boolean(string='Show Login Footer', default=True)
    login_show_db_manager = fields.Boolean(string='Show "Manage Databases" Link', default=True)
    login_footer_text = fields.Char(
        string='Custom Footer Text',
        default='Powered by Odoo 19',
        translate=True
    )

    def action_preview_login_page(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/login',
            'target': 'new',
        }

    def action_reset_login_theme_defaults(self):
        self.ensure_one()
        self.write({
            'login_layout_style': 'split_left',
            'login_card_theme': 'light',
            'login_show_logo': True,
            'login_custom_logo': False,
            'login_bg_type': 'image',
            'login_bg_image': False,
            'login_bg_color_1': '#2e1a47',
            'login_bg_color_2': '#7239ea',
            'login_overlay_opacity': '0.6',
            'login_primary_color': '#7239ea',
            'login_welcome_subtitle': 'Welcome to',
            'login_hero_title': False,
            'login_hero_tagline': 'Sign in to access your business platform.',
            'login_show_footer': True,
            'login_show_db_manager': True,
            'login_footer_text': 'Powered by Odoo 19',
        })
        return True
