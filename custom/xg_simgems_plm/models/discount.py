# -*- coding: utf-8 -*-

from odoo import models, fields, api


# plm/models/discount_indirect.py
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

class DiscountDiscount(models.Model):
    _name = 'discount.discount'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Discount Discount'
    _order = 'name'

    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New',tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,tracking=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user,tracking=True)
    approved_user_id = fields.Many2one('res.users', string='Approved By',tracking=True)
    approved_date = fields.Date(string='Approved Date',tracking=True)
    tags = fields.Many2many('res.partner.category', string='Tags',tracking=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'In Progress'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft',tracking=True)
    
    line_items = fields.One2many('discount.discount.line', 'discount_id', string='Line Items')


    @api.onchange('discount_id')
    def _onchange_discount_id(self):
        if self.discount_id and self.discount_id.attribute_type:
            # Apply the domain based on the attribute_type of the parent record
            return {
                'domain': {
                    'attribute_id': [
                        ('attribute_id.y_attribute_type', '=', self.discount_id.attribute_type)
                    ]
                }
            }
        
    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(DiscountDiscount, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('discount.discount') or 'New'
        return super(DiscountDiscount, self).create(vals)
    
    def action_inprogress(self):
        for data in self:
            data.state = 'inprogress'

    def action_approve(self):
        for data in self:
            data.state = 'approved'
            data.approved_date = date.today()
            data.approved_user_id = self.env.user

    def action_cancel(self):
        for data in self:
            data.state = 'cancel'

    def action_reset_to_draft(self):
        for data in self:
            data.state = 'draft'

    

class DiscountDiscountLine(models.Model):
    _name = 'discount.discount.line'
    _description = 'Discount Line'

    discount_id = fields.Many2one('discount.discount', string='discount Discount', ondelete='cascade')
    attribute_id = fields.Many2one('product.attribute',string='Attribute')
    attribute_value_id = fields.Many2one('product.attribute.value',string='Attribute value')
    discount = fields.Float(string='Discount %',digits=0.00)


    @api.constrains('attribute_id', 'attribute_value_id')
    def _check_unique_attribute_value(self):
        for record in self:
            duplicates = self.search([
                ('id', '!=', record.id),
                ('discount_id', '=', record.discount_id.id),
                ('attribute_id', '=', record.attribute_id.id),
                ('attribute_value_id', '=', record.attribute_value_id.id),
            ])
            if duplicates:
                raise ValidationError(
                    "The combination of Attribute and Attribute Value must be unique."
                )