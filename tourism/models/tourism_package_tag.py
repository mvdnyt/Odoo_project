from odoo import fields, models

class TourismPackageTag(models.Model):
    _name = "tourism.package.tag"
    _description = "Tourism Package Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(string="Active", default=True)