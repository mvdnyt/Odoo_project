from odoo import models, fields, api

class TourismBookingAccount(models.Model):
    _inherit = 'tourism.booking'

    invoice_ids = fields.Many2many(
        'account.move',
        string='Invoices'
    )
    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count'
    )

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def action_create_invoice(self):
        for record in self:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.env.user.partner_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': record.name,
                    'quantity': 1,
                    'price_unit': record.total_amount,
                })]
            })
            record.invoice_ids = [(4, invoice.id)]
