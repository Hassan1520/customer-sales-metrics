from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # إضافة store=True مهم جداً عشان الـ Filter والـ XML اللي عملناه
    total_sales = fields.Float(
        string="Total Sales",
        compute='_compute_sales_metrics',
        store=True
    )
    order_count = fields.Integer(
        string="Order Count",
        compute='_compute_sales_metrics',
        store=True
    )

    # لاحظ هنا: شلنا الـ depends اللي كانت عاملة المشكلة
    # أو ممكن نربطها بـ sale_order_ids لو الموديول بتاعك بيعتمد على sale
    def _compute_sales_metrics(self):
        # 1. تجميع الـ IDs
        partner_ids = self.ids

        # 2. جلب البيانات بـ read_group
        sales_data = self.env['sale.order'].read_group(
            domain=[
                ('partner_id', 'in', partner_ids),
                ('state', 'in', ['sale', 'done'])
            ],
            fields=['amount_total', 'partner_id'],
            groupby=['partner_id']
        )

        # 3. تحويل النتائج لقاموس
        mapped_data = {
            data['partner_id'][0]: {
                'total_sales': data['amount_total'],
                'order_count': data['partner_id_count']
            } for data in sales_data
        }

        # 4. التوزيع على السجلات
        for rec in self:
            data = mapped_data.get(rec.id, {'total_sales': 0.0, 'order_count': 0})
            rec.total_sales = data['total_sales']
            rec.order_count = data['order_count']