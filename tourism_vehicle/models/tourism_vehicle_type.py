from odoo import models, fields


class TourismVehicleType(models.Model):
    _name = "tourism.vehicle.type"
    _description = "Vehicle Type"

    name = fields.Char(required=True)
    vehicle_ids = fields.One2many("tourism.vehicle", "vehicle_type_id", string="Vehicles")
