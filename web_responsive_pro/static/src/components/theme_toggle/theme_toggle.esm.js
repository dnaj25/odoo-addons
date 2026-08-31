/* Copyright 2026 Antigravity
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { cookie } from "@web/core/browser/cookie";

export class ThemeToggle extends Component {
    static props = {};
    setup() {
        this.isDark = cookie.get("color_scheme") === "dark";
    }

    toggle() {
        const nextScheme = this.isDark ? "light" : "dark";
        cookie.set("color_scheme", nextScheme, 365 * 24 * 60 * 60, "path=/");
        if (nextScheme === "dark") {
            document.documentElement.setAttribute("data-bs-theme", "dark");
            document.documentElement.setAttribute("data-color-scheme", "dark");
            document.body?.classList.add("o_dark_theme");
        } else {
            document.documentElement.setAttribute("data-bs-theme", "light");
            document.documentElement.setAttribute("data-color-scheme", "light");
            document.body?.classList.remove("o_dark_theme");
        }
        window.location.reload();
    }
}

ThemeToggle.template = xml`
    <div class="o_theme_toggle d-flex align-items-center justify-content-center" t-on-click="toggle" title="Toggle Dark/Light Mode">
        <button class="btn btn-link text-white p-0 border-0 d-flex align-items-center justify-content-center" style="width: 100%; height: 100%; box-shadow: none;">
            <i t-attf-class="fa fa-lg text-white {{ isDark ? 'fa-sun-o' : 'fa-moon-o' }}"/>
        </button>
    </div>
`;

registry.category("systray").add("ThemeToggle", { Component: ThemeToggle }, { sequence: 99 });
