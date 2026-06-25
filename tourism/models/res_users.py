from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    # Links agent profiles directly to their assigned tour bookings
    tour_booking_ids = fields.One2many(
        "tourism.booking", 
        "create_uid", 
        string="Agent Handled Bookings", 
        readonly=True
    )