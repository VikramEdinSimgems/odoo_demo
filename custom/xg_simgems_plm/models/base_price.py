# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class BasePrice(models.Model):
    _name = 'base.price'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Base Discount'
    _order = 'name'

    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New',tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,tracking=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user,tracking=True)
    approved_user_id = fields.Many2one('res.users', string='Approved By',tracking=True)
    approved_date = fields.Date(string='Approved Date',tracking=True)
    tags = fields.Many2many('res.partner.category', string='Tags',tracking=True)
    weightage_id = fields.Many2one('plm.weightage','Weightage')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'In Progress'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft',tracking=True)
    line_items = fields.One2many('base.price.line', 'base_price_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(BasePrice, self).unlink()

    
    def action_inprogress(self):
        for data in self:
            data.state = 'inprogress'

    def action_approve(self):
        for data in self:
            if data.name == 'New':
                data.name = self.env['ir.sequence'].next_by_code('base.discount') or 'New'
            data.state = 'approved'
            data.approved_date = date.today()
            data.approved_user_id = self.env.user

    def action_cancel(self):
        for data in self:
            data.state = 'cancel'

    def action_reset_to_draft(self):
        for data in self:
            data.state = 'draft'

    

class BasePriceLine(models.Model):
    _name = 'base.price.line'
    _description = 'Base Price Line'

    base_price_id = fields.Many2one('base.price', string='Base Price', ondelete='cascade')
    state = fields.Selection(related='base_price_id.state',string="Status",store=True)
    approved_date = fields.Date(related='base_price_id.approved_date',string='Approved Date',store=True)
    weightage = fields.Float(related='base_price_id.weightage_id.weightage',store=True)
    size_from_id = fields.Many2one('product.attribute.value',string='From Size',domain="[('attribute_id.y_attribute_type', '=', 'size')]")
    size_to_id = fields.Many2one('product.attribute.value',string='To Size',domain="[('attribute_id.y_attribute_type', '=', 'size')]")
    shape_id = fields.Many2one('product.attribute.value',string='Shape',domain="[('attribute_id.y_attribute_type', '=', 'shape')]")
    colour_id = fields.Many2one('product.attribute.value',string='Colour',domain="[('attribute_id.y_attribute_type', '=', 'color')]")
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity',domain="[('attribute_id.y_attribute_type', '=', 'clarity')]")
    cut_id = fields.Many2one('product.attribute.value',string='Cut',domain="[('attribute_id.y_attribute_type', '=', 'cut')]")
    polish_id = fields.Many2one('product.attribute.value',string='Polish',domain="[('attribute_id.y_attribute_type', '=', 'polish')]")
    symmetry_id = fields.Many2one('product.attribute.value',string='Symmetry',domain="[('attribute_id.y_attribute_type', '=', 'sym')]")
    florescence_id = fields.Many2one('product.attribute.value',string='Florescence',domain="[('attribute_id.y_attribute_type', '=', 'florescence')]")
    price_per_carat = fields.Float(string='Price',digits=0.00)
    final_price = fields.Float('Final Price',compute="_compute_final_price")
    
    # Size Overlaping Constrains
    @api.constrains('size_from_id', 'size_to_id')
    def _check_size_overlap(self):
        for record in self:
            if record.size_from_id.y_sequence_no > record.size_to_id.y_sequence_no:
                raise ValidationError(
                    "The 'From Size' sequence must be less than the 'To Size' sequence."
                )

            overlapping_records = self.search([
                ('id', '!=', record.id),
                ('base_price_id', '=', record.base_price_id.id),
                ('size_from_id.y_sequence_no', '<=', record.size_to_id.y_sequence_no),
                ('size_to_id.y_sequence_no', '>=', record.size_from_id.y_sequence_no),
                ('shape_id', '=', record.shape_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('polish_id', '=', record.polish_id.id),
                ('symmetry_id', '=', record.symmetry_id.id),
                ('cut_id', '=', record.cut_id.id),
                ('florescence_id', '=', record.florescence_id.id),
            ])
            if overlapping_records:
                raise ValidationError(
                    "The size range overlaps with another record. Please adjust 'From Size' and 'To Size'."
                )

    # Duplicate Combination Constrains
    @api.constrains('size_from_id', 'size_to_id','shape_id', 'colour_id', 'polish_id', 'clarity_id', 'symmetry_id', 'florescence_id','cut_id')
    def _check_duplicate_combination(self):
        for record in self:
            domain = [
                ('size_from_id', '=', record.size_from_id.id),
                ('size_to_id', '=', record.size_to_id.id),
                ('shape_id', '=', record.shape_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('polish_id', '=', record.polish_id.id),
                ('symmetry_id', '=', record.symmetry_id.id),
                ('cut_id', '=', record.cut_id.id),
                ('florescence_id', '=', record.florescence_id.id),
                ('florescence_id', '=', record.florescence_id.id),
                ('id', '!=', record.id),  # Exclude the current record
                ('base_price_id', '=', record.base_price_id.id)
            ]
            if self.search_count(domain):
                raise ValidationError(
                    "A record with the same combination of Size, Shape, Cut, Colour, Clarity, Polish, Symmetry, and Fluorescence already exists."
                )
            
    @api.depends('price_per_carat','weightage')
    def _compute_final_price(self):
        for data in self:
            data.final_price = data.price_per_carat * data.weightage if data.weightage != 0 else data.price_per_carat
