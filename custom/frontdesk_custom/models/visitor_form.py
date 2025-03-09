# -*- coding: utf-8 -*-
from odoo import fields, models,api, _
from odoo.exceptions import ValidationError, UserError
import re

class FrontdeskVisitor(models.Model):
    _inherit = 'frontdesk.visitor'

    # Get from ocn service when any device registered.
    kam_id = fields.Many2one('frontdesk.kma', string="Key Account Manager")
    Employees_id=fields.Many2one('Frontdesk.Employees',string="Employee Name")
    phone = fields.Char(string="Phone")
    name = fields.Char(string="Name", required=True)


    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if len(record.name) > 16:
                raise ValidationError("Name cannot exceed 16 characters.")
            if not re.match(r'^[A-Za-z0-9\- ]+$', record.name):
                raise ValidationError(
                    "Name can only contain alphabets, numbers, and '-' (hyphen). Special characters are not allowed.")

    @api.model_create_multi
    def create(self, vals):
        """Override create method to delete duplicate records"""
        visitor = super(FrontdeskVisitor, self).create(vals)

        # Find duplicates based on email, phone, or station_id
        duplicate_visitors = self.sudo().search([
            ('email', '=', visitor.email),
            ('phone', '=', visitor.phone),
            ('station_id', '=', visitor.station_id.id),  # Ensure station_id is checked properly
        ], order="create_date DESC")

        if len(duplicate_visitors) > 1:
            oldest_visitor = duplicate_visitors[-1]  # Last record in descending order (oldest)
            latest_visitor = duplicate_visitors[0]  # First record (most recent)

            # If the latest visitor has no kam_id but the oldest does, update it
            if not latest_visitor.kam_id and oldest_visitor.kam_id:
                latest_visitor.sudo().write({'kam_id': oldest_visitor.kam_id})

            # If the latest visitor has no Employees_id but the oldest does, update it
            if not latest_visitor.Employees_id and oldest_visitor.Employees_id:
                latest_visitor.sudo().write({'Employees_id': oldest_visitor.Employees_id})

            oldest_visitor.sudo().unlink()

        return visitor