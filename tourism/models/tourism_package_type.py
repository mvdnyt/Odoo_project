from odoo import fields, models

class TourismPackageType(models.Model):
    _name = "tourism.package.type"
    _description = "Tourism Package Type"
    _order = "name"

    name = fields.Char(string="Package Type", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    active = fields.Boolean(string="Active", default=True)