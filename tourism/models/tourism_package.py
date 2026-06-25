from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class TourismPackage(models.Model):
    _name = "tourism.package"
    _description = "Tourism Package Template"
    _order = "id desc"

    name = fields.Char(string="Package Name", required=True, translate=True)
    description = fields.Text(string="Overview")
    active = fields.Boolean(string="Active", default=True)
    
    # Pricing & Duration
    base_price = fields.Float(string="Base Price (AED)", required=True, default=100.0)
    duration_days = fields.Integer(string="Duration (Days)", default=1, required=True)
    
    # Booking & Contact Details
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    contact_phone = fields.Char(string="Contact Phone")
    contact_email = fields.Char(string="Contact Email")
    passenger_count = fields.Integer(string="Number of Passengers", default=1)
    
    # Existing Relations
    package_type_id = fields.Many2one("tourism.package.type", string="Package Type", ondelete='set null')
    tag_ids = fields.Many2many("tourism.package.tag", string="Marketing Badges")
    
    # Hotel & Dining
    hotel_star_rating = fields.Selection([
        ('3', '3-Star Budget Properties'),
        ('4', '4-Star Premium Selections'),
        ('5', '5-Star Luxury Resorts')
    ], string="Hotel Tier", default='4', required=True)
    
    boarding_type = fields.Selection([
        ('half', 'Half-Board (Breakfast + Dinner)'),
        ('full', 'Full-Board (All 3 Meals Included)')
    ], string="Boarding Criteria", default='half', required=True)
    
    itinerary_day_ids = fields.One2many(
        "tourism.package.day", 
        "package_id", 
        string="Day-by-Day Progression Timeline"
    )

    image_1920 = fields.Image(string="Package Cover Image", max_width=1920, max_height=1920)

    # Validation: Ensure Start Date is before End Date
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError(_("The start date must be before the end date."))

class TourismPackageDay(models.Model):
    _name = "tourism.package.day"
    _description = "Tourism Package Day Schedule"
    _order = "day_number, id"

    package_id = fields.Many2one(
        "tourism.package", 
        string="Parent Package Link", 
        ondelete="cascade", 
        index=True, 
        required=True
    )
    day_number = fields.Integer(string="Day Number", default=1, required=True)
    title = fields.Char(string="Daily Milestone Title", required=True)
    narrative = fields.Text(string="Activity Details")
    is_veg_friendly = fields.Boolean(string="Vegetarian Friendly", default=False)