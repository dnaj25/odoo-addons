import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";

export class SwitchAIDashboard extends Component {
    static template = "switch_ai_dashboard.DashboardTemplate";

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            metrics: {
                total_sales: 0.00,
                sales_count: 0,
                total_purchases: 0.00,
                purchases_count: 0,
                total_invoices: 0.00,
                unpaid_invoices: 0.00,
                customer_count: 0,
                chart_data: []
            },
            aiInsights: "",
            loadingAI: false,
            errorMessage: "",
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            const data = await this.orm.call("switch.ai.dashboard", "get_dashboard_data", []);
            this.state.metrics = data;
        } catch (e) {
            console.error("Failed to load dashboard data", e);
            this.state.errorMessage = "Failed to load dashboard metrics from Odoo database.";
        }
    }

    async generateAIInsights() {
        this.state.loadingAI = true;
        this.state.errorMessage = "";
        this.state.aiInsights = "";
        try {
            const res = await this.orm.call("switch.ai.dashboard", "get_ai_insights", []);
            if (res.status === 'success') {
                this.state.aiInsights = res.insights;
            } else {
                this.state.errorMessage = res.message || "Failed to generate AI insights.";
            }
        } catch (e) {
            console.error("Failed to generate AI insights", e);
            this.state.errorMessage = "Failed to communicate with the Google Gemini AI Service.";
        } finally {
            this.state.loadingAI = false;
        }
    }
}

registry.category("actions").add("switch_ai_dashboard.action", SwitchAIDashboard);
