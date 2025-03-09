# -*- coding: utf-8 -*-
# plm/models/discount_indirect.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class RapPrice(models.Model):
    _name = 'rap.price'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Rap Price'


    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New',tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,tracking=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user,tracking=True)
    approved_user_id = fields.Many2one('res.users', string='Approved By',tracking=True,readonly=True)
    approved_date = fields.Date(string='Approved Date',tracking=True,readonly=True)
    tags = fields.Many2many('res.partner.category', string='Tags',tracking=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'Requested'),
        ('approved', 'Approved'),
        ('expired', 'Expired'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft',tracking=True)
    line_items = fields.One2many('rap.price.line', 'rap_id', string='Line Items')

    @api.model
    def create(self, vals):
        approved_records = self.search([('state', '=', 'approved')])
        approved_records.write({'state': 'expired'})
        if 'responsible_user_id' not in vals:
            vals['responsible_user_id'] = self.env.user.id
        if 'date' not in vals:
            vals['date'] = date.today()
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('rap.price') or 'New'
        vals['approved_user_id'] = self.env.user.id
        vals['approved_date'] = date.today()
        vals['state'] = 'approved'
        record =  super(RapPrice, self).create(vals)
        record.message_post(
            body=f"Record created and approved by user: {self.env.user.name}",
            subtype_id=self.env.ref('mail.mt_note').id,
        )
        return record
    

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(RapPrice, self).unlink()
    

    def action_inprogress(self):
        for data in self:
            data.state = 'inprogress'

    def action_approve(self):
        for data in self:
            if self.name == 'New':
                self.name = self.env['ir.sequence'].next_by_code('rap.price') or 'New'
            data.state = 'approved'
            data.approved_date = date.today()
            data.approved_user_id = self.env.user

    def action_cancel(self):
        for data in self:
            data.state = 'cancel'

    def action_reset_to_draft(self):
        for data in self:
            data.state = 'draft'
    

class RapPriceLine(models.Model):
    _name = 'rap.price.line'
    _description = 'Rap Price Line'

    rap_id = fields.Many2one('rap.price', string='Rapprice', ondelete='cascade',index=True)
    from_size_id = fields.Many2one('product.attribute.value',string='From Size',index=True)
    to_size_id = fields.Many2one('product.attribute.value',string='To Size',index=True)
    colour_id = fields.Many2one('product.attribute.value',string='Colour',index=True)
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity',index=True)
    shape_id = fields.Many2one('product.attribute.value',string='Shape',index=True)
    rap_price = fields.Float(string='Rap Price',digits=0.00)
    rap_date = fields.Date('Rap Date')


    @api.constrains('from_size_id', 'to_size_id', 'colour_id', 'clarity_id', 'shape_id')
    def _check_size_and_duplicate_combination(self):
        for record in self:
            # Check size range validity
            if record.from_size_id.y_sequence_no > record.to_size_id.y_sequence_no:
                raise ValidationError(
                    "The 'From Size' sequence must be less than the 'To Size' sequence."
                )

            # Define a domain for checking both overlap and duplicates
            domain = [
                ('id', '!=', record.id),
                ('rap_id', '=', record.rap_id.id),
                ('from_size_id.y_sequence_no', '<=', record.to_size_id.y_sequence_no),
                ('to_size_id.y_sequence_no', '>=', record.from_size_id.y_sequence_no),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('shape_id', '=', record.shape_id.id),
            ]

            if self.search_count(domain):
                raise ValidationError(
                    "The size range overlaps with another record or a record with the same combination of From Size, To Size, Colour, Clarity, and Shape already exists."
                )