# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class DiscountCapping(models.Model):
    _name = 'discount.capping'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Discount Capping'
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
    line_items = fields.One2many('discount.capping.line', 'discount_capping_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError("You can only delete records that are in the 'Draft' stage.")
        return super(DiscountCapping, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('discount.capping') or 'New'
        return super(DiscountCapping, self).create(vals)
    
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

    

class DiscountDirectLine(models.Model):
    _name = 'discount.capping.line'
    _description = 'Discount Capping Line'

    discount_capping_id = fields.Many2one('discount.capping', string='Discount Capping', ondelete='cascade')
    size_id = fields.Many2one('product.attribute.value',string='Size')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    cut_id = fields.Many2one('product.attribute.value',string='Cut')
    polish_id = fields.Many2one('product.attribute.value',string='Polish')
    symmetry_id = fields.Many2one('product.attribute.value',string='Symmetry')
    florescence_id = fields.Many2one('product.attribute.value',string='Florescence')
    discount = fields.Float(string='Discount %',digits=0.00)


    @api.constrains('size_id', 'cut_id', 'colour_id', 'polish_id', 'clarity_id', 'symmetry_id', 'florescence_id')
    def _check_duplicate_combination(self):
        for record in self:
            domain = [
                ('size_id', '=', record.size_id.id),
                ('cut_id', '=', record.cut_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('polish_id', '=', record.polish_id.id),
                ('symmetry_id', '=', record.symmetry_id.id),
                ('florescence_id', '=', record.florescence_id.id),
                ('discount_capping_id', '=', record.discount_capping_id.id),
                ('id', '!=', record.id)  # Exclude the current record
            ]
            if self.search_count(domain):
                raise ValidationError(
                    "A record with the same combination of Size, Cut, Colour, Clarity, Polish, Symmetry, and Fluorescence already exists.")