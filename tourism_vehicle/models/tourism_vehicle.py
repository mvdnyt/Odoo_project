from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class TourismVehicle(models.Model):
    _name = "tourism.vehicle"
    _description = "Tourism Vehicle"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Info
    name = fields.Char(string="Vehicle Name", required=True)
    license_plate = fields.Char(required=True)
    capacity = fields.Integer(string="Passenger Capacity", required=True)
    vehicle_type_id = fields.Many2one("tourism.vehicle.type", string="Vehicle Type", required=True)

    # Ownership
    ownership = fields.Selection(
        selection=[('internal', 'Internal (Agency Owned)'), ('partner', 'Third-Party (Taxi Partner)')],
        required=True,
        default='internal',
        string="Ownership"
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Taxi Partner Company",
        invisible="ownership == 'internal'"
    )
    commission_rate = fields.Float(
        string="Commission Rate (%)",
        invisible="ownership == 'internal'"
    )

    # Driver
    driver_id = fields.Many2one('res.partner', string="Driver")

    # State
    state = fields.Selection(
        selection=[
            ('available', 'Available'),
            ('on_trip', 'On Trip'),
            ('maintenance', 'Under Maintenance'),
            ('retired', 'Retired'),
        ],
        default='available',
        required=True,
        tracking=True
    )

    # Trips
    trip_ids = fields.One2many("tourism.trip", "vehicle_id", string="Trips")
    total_trips = fields.Integer(compute="_compute_total_trips", string="Total Trips")

    # Maintenance
    last_service_date = fields.Date(string="Last Service Date")
    next_service_date = fields.Date(string="Next Service Date")
    notes = fields.Text()

    @api.depends("trip_ids")
    def _compute_total_trips(self):
        for record in self:
            record.total_trips = len(record.trip_ids)

    def action_set_available(self):
        for record in self:
            if record.state == 'retired':
                raise UserError("A retired vehicle cannot be set as available.")
            record.state = 'available'

    def action_set_maintenance(self):
        for record in self:
            if record.state == 'retired':
                raise UserError("A retired vehicle cannot be sent to maintenance.")
            record.state = 'maintenance'

    def action_retire(self):
        for record in self:
            if record.state == 'on_trip':
                raise UserError("Cannot retire a vehicle that is currently on a trip.")
            record.state = 'retired'

    _check_capacity = models.Constraint(
        'CHECK(capacity > 0)',
        'Passenger capacity must be greater than zero.'
    )
    _check_commission = models.Constraint(
        'CHECK(commission_rate >= 0 AND commission_rate <= 100)',
        'Commission rate must be between 0 and 100.'
    )

    @api.constrains('ownership', 'partner_id')
    def _check_partner_required(self):
        for record in self:
            if record.ownership == 'partner' and not record.partner_id:
                raise ValidationError("A Taxi Partner Company must be set for third-party vehicles.")
