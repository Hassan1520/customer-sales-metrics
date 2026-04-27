from odoo import models, fields, api


class CustomerMetrics(models.Model):
    _name = 'res.partner.customer.metrics'
    _description = 'Customer Sales Metrics'

    customer_id = fields.Many2one('res.partner', string="Customer", required=True)

    total_sales = fields.Float(
        string="Total Sales",
        compute='_compute_metrics',
        store=True
    )

    order_count = fields.Integer(
        string="Order Count",
        compute='_compute_metrics',
        store=True
    )

    @api.depends('customer_id')
    def _compute_metrics(self):
        for rec in self:
            orders = self.env['sale.order'].search([
                ('partner_id', '=', rec.customer_id.id),
                ('state', 'in', ['sale', 'done'])
            ])

            rec.total_sales = sum(orders.mapped('amount_total'))
            rec.order_count = len(orders)

    def get_top_customers(self):
        records = self.search([], order='total_sales desc', limit=5)

        result = []
        for rec in records:
            result.append({
                'name': rec.customer_id.name,
                'total_sales': rec.total_sales,
                'order_count': rec.order_count,
            })

        return result
