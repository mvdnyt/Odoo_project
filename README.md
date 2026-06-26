# Dubai Tourism ERP — Odoo 19
 
A comprehensive Tourism Management ERP system built on Odoo 19, developed as part of an Odoo development training program to digitize and centralize the operations of a Dubai-based tourism agency.
 
##  Project Overview
 
Dubai's tourism industry is one of the fastest-growing in the world, and agencies are constantly overwhelmed by the volume of tourist requests, bookings, and logistics. This ERP system replaces the agency's manual phone-based appointment system with a fully integrated digital platform that manages every aspect of the business — from tour package creation to vehicle dispatch and payment processing.
 
##  Business Goals
 
- Replace manual phone bookings with a centralized reservation system
- Manage internal fleet (buses and vans) and coordinate with third-party taxi partners
- Apply automatic discounts for families with children and groups of 10 or more tourists
- Track revenue from tour package sales and transportation commissions
- Provide management with analytical tools to monitor performance and make data-driven decisions
##  Modules
 
### `dubai_tourism` — Core Tourism Module
The main module covering all primary business operations:
- **Tour Package Management** — create and manage packages with pricing, capacity, duration, destinations, and itineraries
- **Customer Bookings** — full booking lifecycle from draft to completion, with automatic group and family discount calculations
- **Vehicle Fleet Management** — manage internal buses and vans with seat capacity, state tracking, and utilization reporting
- **Transport Assignment** — assign internal vehicles or third-party taxis to bookings, track costs and commissions
- **Destination Management** — maintain a catalog of Dubai tourist destinations linked to packages
- **Departure Scheduling** — schedule group departures with guide assignments and capacity management
- **Customer Reviews** — collect and display ratings and feedback per booking and package
- **Portal Access** — customers can view their bookings online through Odoo's customer portal
- **Automated Notifications** — email templates and scheduled actions for booking reminders and updates
- **Reporting** — printable booking reports and management dashboards
### `tourism_accounts` — Financial Integration Module
Extends the core module with accounting features:
- Automatic invoice generation upon booking confirmation
- Payment tracking and reconciliation
- Commission billing for third-party taxi partner transactions
- Financial reporting tied to booking revenue
##  Transportation Logic
 
The agency operates a mixed transportation model:
- **Internal Fleet** — buses and vans owned by the agency are assigned to large groups (10+ tourists) through the transport assignment system
- **Third-Party Taxis** — small groups, couples, and families are dispatched through a partnered local taxi company, with commission rates tracked per assignment
##  Pricing & Discount Rules
 
| Condition | Discount |
|---|---|
| Group of 10 or more tourists | Group discount applied automatically |
| Family booking with young children | Family discount applied automatically |
| Featured packages | Promotional price override available |
 
##  Analytics & Reporting
 
Management has access to:
- Booking trends by package, destination, and date
- Vehicle utilization rates and seat fill percentages
- Most popular tour packages and destinations
- Revenue breakdown from package sales vs. transport commissions
- Printable booking confirmation reports
##  Tech Stack
 
- **Platform:** Odoo 19 (Community)
- **Language:** Python 3.12
- **Views:** XML (Odoo QWeb)
- **Database:** PostgreSQL
- **Version Control:** Git / GitHub
##  Team
 
This project was built collaboratively, with each team member responsible for a specific domain:
- Tour package and destination management
- Customer bookings and discount logic
- Vehicle and transport management
- Financial integration and invoicing
##  Installation
 
1. Clone this repository into your Odoo Workshop addons folder
2. Restart the Odoo server
3. Go to Apps → Update Apps List
4. Search "Dubai Tourism" → Install
5. Optionally enable demo data for pre-loaded sample records
##  Repository Structure
 
```
├── dubai_tourism/          # Core tourism module
│   ├── models/             # Business logic
│   ├── views/              # UI definitions
│   ├── security/           # Access rights
│   ├── data/               # Sequences, cron jobs, email templates
│   ├── demo/               # Sample data
│   ├── report/             # PDF reports
│   ├── wizard/             # Transport assignment wizard
│   └── controllers/        # Portal controllers
├── tourism_accounts/       # Accounting integration module
└── README.md
```
