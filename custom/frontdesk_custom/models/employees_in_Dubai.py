from odoo import models, fields, api

class FrontdeskEmployees(models.Model):
    _name = "frontdesk.employees"
    _description = "Employees In Dubai Office"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email", required=True)
    name = fields.Char(string="Name", compute="_compute_name", store=True)

    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for record in self:
            if record.first_name and record.last_name:
                record.name = f"{record.first_name} {record.last_name}"
            elif record.first_name:
                record.name = record.first_name
            elif record.last_name:
                record.name = record.last_name
            else:
                record.name = "Employees Name"