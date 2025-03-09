# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from itertools import product

class DiscountDirect(models.Model):
    _name = 'discount.direct'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Discount Direct'
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
    line_items = fields.One2many('discount.direct.line', 'discount_direct_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft' and record.state !='cancel':
                raise ValidationError(
                    "You can only delete records that are in the 'Draft' stage."
                )
        return super(DiscountDirect, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('discount.direct') or 'New'
        return super(DiscountDirect, self).create(vals)
    
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
    _name = 'discount.direct.line'
    _description = 'Discount Direct Line'

    discount_direct_id = fields.Many2one('discount.direct', string='Discount Direct', ondelete='cascade')
    approved_date = fields.Date(string='Approved Date', store=True, related='discount_direct_id.approved_date')
    size_from_id = fields.Many2one('product.attribute.value',string='Size From')
    size_to_id = fields.Many2one('product.attribute.value',string='Size To')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    from_cut_id = fields.Many2one('product.attribute.value',string='From Cut')
    to_cut_id = fields.Many2one('product.attribute.value',string='To Cut')
    from_pol_id = fields.Many2one('product.attribute.value',string='From Pol')
    to_pol_id = fields.Many2one('product.attribute.value',string='To Pol')
    from_sym_id = fields.Many2one('product.attribute.value',string='From Sym')
    to_sym_id = fields.Many2one('product.attribute.value',string='To Sym')
    from_florescence_id = fields.Many2one('product.attribute.value',string='From Flo')
    to_florescence_id = fields.Many2one('product.attribute.value',string='To Flo')
    discount = fields.Float(string='Discount',digits=0.00)

    @api.constrains('size_from_id', 'size_to_id', 
                    'colour_id', 
                    'clarity_id', 
                    'from_cut_id', 'to_cut_id',
                    'from_pol_id', 'to_pol_id',
                    'from_sym_id', 'to_sym_id',
                    'from_florescence_id', 'to_florescence_id'
                    )
    def _check_unique_and_overlap(self):
        for record in self:
            # Ensure `size_from_id` is less than `size_to_id`
            if record.size_from_id.id > record.size_to_id.id:
                raise ValidationError("The 'Size From' value must be less than or equal to 'Size To'.")        
            # Ensure `from_cut_id` is less than `to_cut_id`
            if record.from_cut_id.id > record.to_cut_id.id:
                raise ValidationError("The 'Cut From' value must be less than or equal to 'Cut To'.")
            # Ensure `from_pol_id` is less than `to_pol_id`
            if record.from_pol_id.id > record.to_pol_id.id:
                raise ValidationError("The 'Polish From' value must be less than or equal to 'Polish To'.")
            # Ensure `from_sym_id` is less than `to_sym_id`
            if record.from_sym_id.id > record.to_sym_id.id:
                raise ValidationError("The 'Symmetry From' value must be less than or equal to 'Symmetry To'.")
            # Ensure `from_florescence_id` is less than `to_florescence_id`
            if record.from_florescence_id.id > record.to_florescence_id.id:
                raise ValidationError("The 'Florescence From' value must be less than or equal to 'Florescence To'.")
            
            size_ids = range(record.size_from_id.y_sequence_no, record.size_to_id.y_sequence_no + 1)
            color_ids = range(record.colour_id.y_sequence_no, record.colour_id.y_sequence_no + 1)
            clarity_ids = range(record.clarity_id.y_sequence_no, record.clarity_id.y_sequence_no + 1)
            cut_ids = range(record.from_cut_id.y_sequence_no, record.to_cut_id.y_sequence_no + 1)
            pol_ids = range(record.from_pol_id.y_sequence_no, record.to_pol_id.y_sequence_no + 1)
            sym_ids = range(record.from_sym_id.y_sequence_no, record.to_sym_id.y_sequence_no + 1)
            flo_ids = range(record.from_florescence_id.y_sequence_no, record.to_florescence_id.y_sequence_no + 1)
            # Generate all possible combinations for the current record
            current_combinations = set(product(size_ids, color_ids,clarity_ids,cut_ids,pol_ids,sym_ids,flo_ids))
            # Find overlapping records in the same group
            overlapping_records = self.search([
                ('id', '!=', record.id),
                ('discount_direct_id', '=', record.discount_direct_id.id),
            ])
            for other_record in overlapping_records:
                # Generate ranges for the other record
                other_size_ids = range(other_record.size_from_id.y_sequence_no, other_record.size_to_id.y_sequence_no + 1)
                other_color_ids = range(other_record.colour_id.y_sequence_no, other_record.colour_id.y_sequence_no + 1)
                other_clarity_ids = range(other_record.clarity_id.y_sequence_no, other_record.clarity_id.y_sequence_no + 1)
                other_cut_ids = range(other_record.from_cut_id.y_sequence_no, other_record.to_cut_id.y_sequence_no + 1)
                other_pol_ids = range(other_record.from_pol_id.y_sequence_no, other_record.to_pol_id.y_sequence_no + 1)
                other_sym_ids = range(other_record.from_sym_id.y_sequence_no, other_record.to_sym_id.y_sequence_no + 1)
                other_flo_ids = range(other_record.from_florescence_id.y_sequence_no, other_record.to_florescence_id.y_sequence_no + 1)
                # Generate all possible combinations for the other record
                other_combinations = set(product(other_size_ids, other_color_ids,other_clarity_ids,other_cut_ids,other_pol_ids,other_sym_ids, other_flo_ids))
                # Check for intersection between current and other record combinations
                common_combinations = current_combinations.intersection(other_combinations)
                if common_combinations:
                    raise ValidationError(
                        f"Duplicate combination detected between records {record.id} and {other_record.id}."
                    )
