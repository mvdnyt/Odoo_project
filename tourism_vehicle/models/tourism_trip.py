from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class TourismTrip(models.Model):
    _name = "tourism.trip"
    _description = "Tourism Trip"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Trip Reference", required=True)
    trip_date = fields.Date(string="Trip Date", required=True)
    destination = fields.Char(required=True)
    passenger_count = fields.Integer(string="Number of Passengers", required=True)

    vehicle_id = fields.Many2one("tourism.vehicle", string="Assigned Vehicle", required=True)
    vehicle_capacity = fields.Integer(related="vehicle_id.capacity", string="Vehicle Capacity", readonly=True)
    vehicle_ownership = fields.Selection(related="vehicle_id.ownership", string="Vehicle Ownership", readonly=True)

    # Group type auto-detected
    group_type = fields.Selection(
        selection=[('small', 'Small Group / Family'), ('large', 'Large Group')],
        compute="_compute_group_type",
        store=True,
        string="Group Type"
    )

    # Commission tracking for taxi partner trips
    commission_amount = fields.Float(string="Commission Amount", compute="_compute_commission", store=True)

    state = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled',
        required=True,
        tracking=True
    )

    notes = fields.Text()

    @api.depends("passenger_count")
    def _compute_group_type(self):
        for record in self:
            # Agency rule: 10+ tourists = large group
            record.group_type = 'large' if record.passenger_count >= 10 else 'small'

    @api.depends("vehicle_id.commission_rate", "passenger_count", "vehicle_id.ownership")
    def _compute_commission(self):
        for record in self:
            if record.vehicle_id.ownership == 'partner':
                # Simple flat commission per passenger based on rate
                record.commission_amount = (record.vehicle_id.commission_rate / 100) * record.passenger_count * 10
            else:
                record.commission_amount = 0.0

    def action_start_trip(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cannot start a cancelled trip.")
            record.vehicle_id.state = 'on_trip'
            record.state = 'ongoing'

    def action_complete_trip(self):
        for record in self:
            if record.state != 'ongoing':
                raise UserError("Only ongoing trips can be marked as completed.")
            record.vehicle_id.state = 'available'
            record.state = 'completed'

    def action_cancel_trip(self):
        for record in self:
            if record.state == 'completed':
                raise UserError("Completed trips cannot be cancelled.")
            if record.vehicle_id.state == 'on_trip':
                record.vehicle_id.state = 'available'
            record.state = 'cancelled'

    @api.constrains("passenger_count", "vehicle_id")
    def _check_capacity(self):
        for record in self:
            if record.passenger_count > record.vehicle_id.capacity:
                raise ValidationError(
                    f"Passenger count ({record.passenger_count}) exceeds "
                    f"vehicle capacity ({record.vehicle_id.capacity}) for {record.vehicle_id.name}."
                )

    @api.constrains("vehicle_id", "trip_date", "state")
    def _check_vehicle_availability(self):
        for record in self:
            if record.state in ('scheduled', 'ongoing'):
                conflict = self.search([
                    ('vehicle_id', '=', record.vehicle_id.id),
                    ('trip_date', '=', record.trip_date),
                    ('state', 'in', ['scheduled', 'ongoing']),
                    ('id', '!=', record.id),
                ])
                if conflict:
                    raise ValidationError(
                        f"Vehicle {record.vehicle_id.name} is already assigned to another trip on {record.trip_date}."
                    )
