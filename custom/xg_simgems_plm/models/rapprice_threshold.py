# -*- coding: utf-8 -*-
# plm/models/discount_indirect.py

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class RappriceThreshold(models.Model):
    _name = 'rapprice.threshold'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Rapprice Threshold'


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
    line_items = fields.One2many('rapprice.threshold.line', 'rapprice_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(RappriceThreshold, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('rapprice.threshold') or 'New'
        return super(RappriceThreshold, self).create(vals)
    

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
    

class RappriceThresholdLine(models.Model):
    _name = 'rapprice.threshold.line'
    _description = 'Rapprice Threshold Line'

    rapprice_id = fields.Many2one('rapprice.threshold', string='Rapprice', ondelete='cascade')
    from_size_id = fields.Many2one('product.attribute.value',string='From Size')
    to_size_id = fields.Many2one('product.attribute.value',string='To Size')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    threshold_rap_price = fields.Float(string='Tshld Rap Price',digits=0.00)

    @api.constrains('from_size_id', 'to_size_id')
    def _check_size_overlap(self):
        for record in self:
            if record.from_size_id.y_sequence_no > record.to_size_id.y_sequence_no:
                raise ValidationError(
                    "The 'From Size' sequence must be less than the 'To Size' sequence."
                )

            overlapping_records = self.search([
                ('id', '!=', record.id),('rapprice_id','=',record.rapprice_id.id),
                ('from_size_id.y_sequence_no', '<=', record.to_size_id.y_sequence_no),
                ('to_size_id.y_sequence_no', '>=', record.from_size_id.y_sequence_no),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('shape_id', '=', record.shape_id.id),
            ])
            if overlapping_records:
                raise ValidationError(
                    "The size range overlaps with another record. Please adjust 'From Size' and 'To Size'."
                )

    @api.constrains('from_size_id', 'to_size_id', 'colour_id', 'clarity_id', 'shape_id')
    def _check_duplicate_combination(self):
        for record in self:
            domain = [
                ('from_size_id', '=', record.from_size_id.id),
                ('to_size_id', '=', record.to_size_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('shape_id', '=', record.shape_id.id),
                ('rapprice_id','=',record.rapprice_id.id),
                ('id', '!=', record.id)  # Exclude the current record
            ]
            if self.search_count(domain):
                raise ValidationError(
                    "A record with the same combination of From Size, To Size, Colour, Clarity, and Shape already exists."
                )