# Copyright 2023 Taras Shabaranskyi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def color_scheme(self):
        print("WEB_RESPONSIVE_PRO COLOR_SCHEME CALLED!")
        from odoo.http import request
        if request:
            print("Request exists.")
            if hasattr(request, 'httprequest') and request.httprequest:
                print("httprequest exists.")
                # request.httprequest.cookies can be a dict or a Werkzeug ImmutableTypeConversionDict
                cookies = getattr(request.httprequest, 'cookies', None)
                if cookies:
                    print("cookies exist in request:", cookies)
                    cookie_scheme = cookies.get('color_scheme')
                    print("cookie_scheme is:", cookie_scheme)
                    if cookie_scheme in ('light', 'dark'):
                        return cookie_scheme
        return super().color_scheme()

    def session_info(self):
        session = super().session_info()
        user = self.env.user
        return {
            **session,
            "apps_menu": {
                "search_type": user.apps_menu_search_type,
                "theme": user.apps_menu_theme,
            },
        }
