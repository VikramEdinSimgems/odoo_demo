# -*- coding: utf-8 -*-

from odoo import models, fields, api


# plm/models/discount_indirect.py
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

class InternalDiscount(models.Model):
    _name = 'internal.discount'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Internal Discount'
    _order = 'name'

    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New',tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,tracking=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user,tracking=True)
    approved_user_id = fields.Many2one('res.users', string='Approved By',tracking=True)
    approved_date = fields.Date(string='Approved Date',tracking=True)
    tags = fields.Many2many('res.partner.category', string='Tags',tracking=True)
    weightage_id = fields.Many2one('plm.weightage','Weightage')
    country_id = fields.Many2one(  # used to filter the available internal discount depending on the country.
        comodel_name='res.country',required=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'In Progress'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft',tracking=True)
    line_items = fields.One2many('internal.discount.line', 'internal_discount_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(InternalDiscount, self).unlink()
    
    
    def action_inprogress(self):
        for data in self:
            data.state = 'inprogress'

    def action_approve(self):
        for data in self:
            if data.name == 'New':
                data.name = self.env['ir.sequence'].next_by_code('internal.discount') or 'New'
            data.state = 'approved'
            data.approved_date = date.today()
            data.approved_user_id = self.env.user

    def action_cancel(self):
        for data in self:
            data.state = 'cancel'

    def action_reset_to_draft(self):
        for data in self:
            data.state = 'draft'

    

class InternalDiscountLine(models.Model):
    _name = 'internal.discount.line'
    _description = 'Internal Discount Line'

    internal_discount_id = fields.Many2one('internal.discount', string='Internal Discount', ondelete='cascade')
    state = fields.Selection(related='internal_discount_id.state',string="Status",store=True)
    approved_date = fields.Date(related='internal_discount_id.approved_date',string='Approved Date',store=True)
    weightage = fields.Float(related='internal_discount_id.weightage_id.weightage',store=True)
    size_id = fields.Many2one('product.attribute.value',string='Size')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    cut_id = fields.Many2one('product.attribute.value',string='Cut')
    polish_id = fields.Many2one('product.attribute.value',string='Polish')
    symmetry_id = fields.Many2one('product.attribute.value',string='Symmetry')
    florescence_id = fields.Many2one('product.attribute.value',string='Florescence')
    price_per_carat = fields.Float('Price',digits=0.00)
    final_price = fields.Float('Final Price',compute="_compute_final_price")

    @api.constrains('size_id','shape_id', 'cut_id', 'colour_id', 'clarity_id', 'polish_id','florescence_id','symmetry_id')
    def _check_duplicate_combination(self):
        for record in self:
            domain = [
                ('size_id', '=', record.size_id.id),
                ('cut_id', '=', record.cut_id.id),
                ('shape_id', '=', record.shape_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('polish_id', '=', record.polish_id.id),
                ('florescence_id', '=', record.florescence_id.id),
                ('symmetry_id', '=', record.symmetry_id.id),
                ('internal_discount_id','=',record.internal_discount_id.id),
                ('id', '!=', record.id)  # Exclude the current record
            ]
            if self.search_count(domain):
                raise ValidationError(
                    "A record with the same combination of Size, Shape, Colour, Clarity, Cut, Polish, Symmetry and Florescence already exists."
                )

    @api.depends('price_per_carat','weightage')
    def _compute_final_price(self):
        for data in self:
            data.final_price = data.price_per_carat * data.weightage if data.weightage != 0 else 0.00