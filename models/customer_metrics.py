from odoo import models, fields, api


class CustomerMetrics(models.Model):
    _name = 'res.partner.customer.metrics'
    _description = 'Customer Sales Metrics'

    customer_id = fields.Many2one('res.partner', string="Customer")
    total_sales = fields.Float(string="Total Sales", compute='_compute_sales_metrics', store=True)
    order_count = fields.Integer(string="Order Count", compute='_compute_sales_metrics', store=True)

    @api.depends('customer_id')
    def _compute_sales_metrics(self):
        for rec in self:
            if not rec.customer_id:
                rec.total_sales = 0
                rec.order_count = 0
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', rec.customer_id.id),
                ('state', 'in', ['sale', 'done'])
            ])
            rec.total_sales = sum(orders.mapped('amount_total'))
            rec.order_count = len(orders)

    @api.model
    def cron_get_top_customers(self):
        top_sales = self.env['sale.order']._read_group(
            domain=[('state', 'in', ['sale', 'done'])],
            groupby=['partner_id'],
            aggregates=['amount_total:sum'],
            order='amount_total:sum desc',
            limit=5
        )
        current_top_ids = [partner.id for partner, total in top_sales]
        self.search([('customer_id', 'not in', current_top_ids)]).unlink()
        for p_id in current_top_ids:
            if not self.search([('customer_id', '=', p_id)]):
                self.create({'customer_id': p_id})
        return self.env["ir.actions.actions"]._for_xml_id("customer_metrics.action_customer_metrics")

    def action_refresh_now(self):
        self.cron_get_top_customers()
