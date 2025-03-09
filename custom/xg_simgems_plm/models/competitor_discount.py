# -*- coding: utf-8 -*-

# plm/models/discount_indirect.py
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date

class CompetitorDiscount(models.Model):
    _name = 'competitor.discount'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Competitor Discount'
    _order = 'name'

    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New',tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,tracking=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user,tracking=True)
    approved_user_id = fields.Many2one('res.users', string='Approved By',tracking=True)
    approved_date = fields.Date(string='Approved Date',tracking=True)
    tags = fields.Many2many('res.partner.category', string='Tags',tracking=True)
    weightage_id = fields.Many2one('plm.weightage','Weightage',tracking=True)
    competitor_id = fields.Many2one('plm.competitor','Competitor',tracking=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'In Progress'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft',tracking=True)
    line_items = fields.One2many('competitor.discount.line', 'competitor_disc_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft' and record.state !='cancel':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(CompetitorDiscount, self).unlink()

    
    def action_inprogress(self):
        for data in self:
            data.state = 'inprogress'

    def action_approve(self):
        for data in self:
            if data.name == 'New':
                data.name = self.env['ir.sequence'].next_by_code('competitor.discount') or 'New'
            data.state = 'approved'
            data.approved_date = date.today()
            data.approved_user_id = self.env.user

    def action_cancel(self):
        for data in self:
            data.state = 'cancel'

    def action_reset_to_draft(self):
        for data in self:
            data.state = 'draft'

    

class CompetitorDiscountLine(models.Model):
    _name = 'competitor.discount.line'
    _description = 'Competitor Discount Line'

    competitor_disc_id = fields.Many2one('competitor.discount', string='Competitor Discount', ondelete='cascade')
    state = fields.Selection(related='competitor_disc_id.state',string="Status",store=True)
    approved_date = fields.Date(related='competitor_disc_id.approved_date',string='Approved Date',store=True)
    weightage = fields.Float(related='competitor_disc_id.weightage_id.weightage',store=True)
    competitor_id = fields.Many2one(related='competitor_disc_id.competitor_id',store=True)
    size_id = fields.Many2one('product.attribute.value',string='Size')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    cut_id = fields.Many2one('product.attribute.value',string='Cut')
    polish_id = fields.Many2one('product.attribute.value',string='Polish')
    symmetry_id = fields.Many2one('product.attribute.value',string='Symmetry')
    carat_id = fields.Many2one('product.attribute.value',string='Per Carat')
    florescence_id = fields.Many2one('product.attribute.value',string='Florescence')
    price_per_carat = fields.Float('Price',digits=0.00)
    final_price = fields.Float('Final Price',compute="_compute_final_price")

    @api.constrains('size_id','shape_id', 'cut_id', 'colour_id', 'polish_id', 'clarity_id', 'symmetry_id', 'florescence_id','carat_id')
    def _check_duplicate_combination(self):
        for record in self:
            domain = [
                ('competitor_disc_id', '=', record.competitor_disc_id.id),
                ('size_id', '=', record.size_id.id),
                ('shape_id', '=', record.shape_id.id),
                ('cut_id', '=', record.cut_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('polish_id', '=', record.polish_id.id),
                ('symmetry_id', '=', record.symmetry_id.id),
                ('carat_id', '=', record.carat_id.id),
                ('florescence_id', '=', record.florescence_id.id),
                ('florescence_id', '=', record.florescence_id.id),
                ('id', '!=', record.id)  # Exclude the current record
            ]
            if self.search_count(domain):
                raise ValidationError(
                    "A record with the same combination of Size, Shape, Cut, Colour, Clarity, Polish, Symmetry, Carat, and Fluorescence already exists."
                )

    @api.depends('price_per_carat','weightage')
    def _compute_final_price(self):
        for data in self:
            data.final_price = data.price_per_carat * data.weightage if data.weightage != 0 else 0.00