from odoo import fields, models, api
from odoo.exceptions import ValidationError

class TourismBooking(models.Model):
    _name = "tourism.booking"
    _description = "Agent Booking Desk"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    name = fields.Char(string="Booking Reference", required=True, copy=False, readonly=True, default=lambda self: 'NEW')
    
    # Customer Lead Info (Captured by Agent over phone from the customer)
    contact_name = fields.Char(string="Contact Person Name", required=True, tracking=True)
    whatsapp_number = fields.Char(string="WhatsApp Contact", required=True, tracking=True)
    booking_date = fields.Date(string="Target Travel Date", required=True, default=fields.Date.today)
    
    # Age-Group Details
    group_size = fields.Integer(string="Total Number of People", default=1, required=True, tracking=True)
    has_infants = fields.Boolean(string="Toddlers & Infants (<3 yrs)", default=False, tracking=True)
    
    # Emergency Tracking Numbers (Enforced conditionally for child safety)
    emergency_phone_1 = fields.Char(string="Emergency Phone 1")
    emergency_phone_2 = fields.Char(string="Emergency Phone 2")
    emergency_phone_3 = fields.Char(string="Emergency Phone 3")

    # Package Linkages
    package_id = fields.Many2one("tourism.package", string="Selected Dubai Package", required=True)
    hotel_star_rating = fields.Selection(related="package_id.hotel_star_rating", string="Hotel Tier Level", readonly=True)
    boarding_type = fields.Selection(related="package_id.boarding_type", string="Boarding Criteria", readonly=True)

    # Automated Transport Router Logic
    transport_type = fields.Selection([
        ('internal', 'Internal Agency Fleet (Bus/Van)'),
        ('external', 'External Partner Taxi Network')
    ], string="Logistics Routing Allocation", compute="_compute_transport_routing", store=True, readonly=True)
    
    # Fleet link (Visible to agent only if internal fleet is selected)
    vehicle_id = fields.Many2one("fleet.vehicle", string="Assigned Agency Vehicle")
    vehicle_reg_no = fields.Char(related="vehicle_id.license_plate", string="Vehicle Registration Number", readonly=True)

    # Computational Pricing Fields
    gross_amount = fields.Float(string="Gross Cost (AED)", compute="_compute_amounts", store=True)
    discount = fields.Float(string="Applied Markdown Discount (%)", default=0.0, tracking=True)
    total_amount = fields.Float(string="Final Settled Amount (AED)", compute="_compute_amounts", store=True, tracking=True)
    operational_notes = fields.Text(string="Special Logistics Requests Dispatch", compute="_compute_operational_notes", store=True)

    # System State Flow
    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('confirmed', 'Confirmed Booking'),
        ('cancelled', 'Cancelled')
    ], string="Pipeline Status", default='draft', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):  
        for vals in vals_list:
            if vals.get('name', 'NEW') == 'NEW':
                vals['name'] = self.env['ir.sequence'].next_by_code('tourism.booking') or 'NEW'
        return super(TourismBooking, self).create(vals_list)

    @api.depends('group_size')
    def _compute_transport_routing(self):
        """ Automated Fleet Router: Evaluates passenger counts to allocate assets """
        for record in self:
            if record.group_size >= 10:
                record.transport_type = 'internal'
            else:
                record.transport_type = 'external'
                record.vehicle_id = False # Reset asset link if routed to external taxis

    @api.depends('package_id', 'group_size', 'has_infants', 'discount')
    def _compute_amounts(self):
        """ Automated Calculation Engine for base fees and safety discounts """
        for record in self:
            base_rate = record.package_id.base_price if record.package_id else 0.0
            record.gross_amount = base_rate * record.group_size
            
            # Auto-apply 5% infant discount if checked
            applied_discount = record.discount
            if record.has_infants:
                applied_discount = max(applied_discount, 5.0)
            
            record.discount = applied_discount
            record.total_amount = record.gross_amount * (1.0 - (record.discount / 100.0))

    @api.depends('has_infants')
    def _compute_operational_notes(self):
        """ Appends operational flags to the driver dispatch view """
        for record in self:
            if record.has_infants:
                record.operational_notes = "WARNING: INFANTS PRESENT. DRIVER DISPATCH CRITICAL -> Requires Car Seats & Baby Safety Equipment."
            else:
                record.operational_notes = "Standard tour execution parameters apply."

    @api.constrains('has_infants', 'emergency_phone_1', 'emergency_phone_2', 'emergency_phone_3')
    def _check_infant_safety_contacts(self):
        """ Python Safety Constraint: Forces agent to gather 3 backup contacts if an infant is onboard """
        for record in self:
            if record.has_infants:
                if not record.emergency_phone_1 or not record.emergency_phone_2 or not record.emergency_phone_3:
                    raise ValidationError(
                        "INFANT SAFETY ENFORCEMENT RULE:\n"
                        "You must collect exactly 3 alternative phone numbers on the call "
                        "before you can save a booking folder containing toddlers or infants under 3."
                    )

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})