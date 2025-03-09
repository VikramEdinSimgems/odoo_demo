# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class LessDiscount(models.Model):
    _name = 'less.discount'
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
    line_items = fields.One2many('less.discount.line', 'less_discount_id', string='Line Items')

    # Restrict Record Deletion not in draft state
    def unlink(self):
        for record in self:
            if record.state != 'draft' and record.state !='cancel':
                raise ValidationError("You can only delete records that are in the 'Draft' stage.")
        return super(LessDiscount, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('less.discount') or 'New'
        return super(LessDiscount, self).create(vals)

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



class LessDiscountLine(models.Model):
    _name = 'less.discount.line'
    _description = 'Discount Direct Line'

    less_discount_id = fields.Many2one('less.discount', string='Discount Direct', ondelete='cascade')
    size_id = fields.Many2one('product.attribute.value',string='Size')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    cut_id = fields.Many2one('product.attribute.value',string='Cut')
    polish_id = fields.Many2one('product.attribute.value',string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value',string='Sym')
    florescence_id = fields.Many2one('product.attribute.value',string='Florescence')
    base_per_carat = fields.Float(string='Base Per Carat',digits=0.00)
    rap = fields.Float(string='Rap',digits=0.00,compute='_compute_rap_price')
    avg_per_carat = fields.Float(string='Avg P.CT',digits=0.00,compute='_compute_avg_per_carat', store=True)
    avg_rap_back = fields.Float(string='Avg Rap Back',digits=0.00, compute='_compute_avg_rap_back')
    total_weightage = fields.Float('Total Weigtage',readonly=True,store=True)


    # Alternative Python-based validation for additional control
    @api.constrains('size_id','shape_id', 'colour_id', 'clarity_id', 'cut_id', 'polish_id', 'symmetry_id', 'florescence_id')
    def _check_unique_combination(self):
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('less_discount_id', '=', record.less_discount_id.id),
                ('size_id', '=', record.size_id.id),
                ('shape_id', '=', record.shape_id.id),
                ('colour_id', '=', record.colour_id.id),
                ('clarity_id', '=', record.clarity_id.id),
                ('cut_id', '=', record.cut_id.id),
                ('polish_id', '=', record.polish_id.id),
                ('symmetry_id', '=', record.symmetry_id.id),
                ('florescence_id', '=', record.florescence_id.id)
            ]
            if self.search_count(domain):
                raise ValidationError('A discount line with this combination of attributes already exists.')

    @api.depends('size_id','shape_id', 'colour_id', 'clarity_id', 'cut_id', 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_avg_per_carat(self):
        for record in self:
            total_weightage = 0.00
            if all([record.size_id,record.shape_id, record.colour_id, record.clarity_id, record.cut_id, record.polish_id, record.symmetry_id, record.florescence_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
                base_domain = [
                    ('size_from_id.y_sequence_no', '<=', size_sequence),
                    ('size_to_id.y_sequence_no', '>=', size_sequence),
                    ('shape_id', '=', record.shape_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    ('base_price_id.state','=','approved')
                ]
                # Build the domain for the base price
                competitor_domain = [
                    ('size_id', '=', record.size_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    ('competitor_disc_id', '!=',False ),
                    ('state','=','approved')
                ]
                # Search for the matching record in `base.price.line`
                base_price_line = self.env['base.price.line'].search(base_domain,order='approved_date desc', limit=1)
                total_weightage += base_price_line.weightage
                # Search for the matching record in `competitor.discount.line`
                competitor_price = 0
                matching_competitor_price_line = self.env['competitor.discount.line'].search(competitor_domain,order='approved_date desc')
                if matching_competitor_price_line:
                    # Group matching lines by country_id and compute averages
                    competitor_data = {}
                    for line in matching_competitor_price_line:
                        competitor = line.competitor_disc_id.competitor_id.id
                        if competitor not in competitor_data:
                            competitor_data[competitor] = []
                            total_weightage += line.weightage
                            competitor_data[competitor].append(line.final_price)
                    
                    # Compute Total across all competitors
                    total_price = 0
                    for prices in competitor_data.values():
                        total_price += sum(prices)
                    
                    # Final value: Total average across all competitors
                    competitor_price = total_price
                # Build the domain to find matching `internal.discount.line` records
                internal_domain = [
                    ('size_id', '=', record.size_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    ('internal_discount_id.state','=','approved')
                ]
                internal_price = 0
                # Search for matching internal discount lines
                matching_internal_discount_lines = self.env['internal.discount.line'].search(internal_domain,order='approved_date desc')
                if matching_internal_discount_lines:
                    # Group matching lines by country_id and compute averages
                    country_data = {}
                    for line in matching_internal_discount_lines:
                        country = line.internal_discount_id.country_id
                        if country not in country_data:
                            country_data[country] = []
                            country_data[country].append(line.final_price)
                            total_weightage += line.weightage
                    
                    # Compute Total across all countries
                    total_internal_price = 0
                    for prices in country_data.values():
                        total_internal_price += sum(prices)

                    internal_price = total_internal_price
                base_price_per_carat = base_price_line.final_price
                sum_of_prices = internal_price + base_price_per_carat + competitor_price
                record.avg_per_carat =  sum_of_prices/total_weightage if sum_of_prices != 0 and total_weightage != 0 else 0.00
            else:
                record.avg_per_carat = 0.0

    @api.depends('size_id', 'colour_id', 'clarity_id', 'cut_id', 'polish_id', 'symmetry_id', 'florescence_id',
                 'shape_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id, record.cut_id, record.polish_id,
                    record.symmetry_id, record.florescence_id, record.shape_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id

                # Base domain
                domain = [
                    ('from_size_id.y_sequence_no', '<=', size_sequence),
                    ('to_size_id.y_sequence_no', '>=', size_sequence),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('rap_id.state', '=', 'approved')
                ]

                # Shape-based condition

                if record.shape_id.name.lower() == 'round':
                    domain.append(('shape_id', '=', record.shape_id.id))  # Fetch round rap price
                else:
                    fancy_shapes = [
                        'pear', 'emerald', 'princess', 'cushion', 'oval', 'heart', 'marquise',
                        'cushion-modified', 'cushion-brilliant', 'radiant', 'radiant-modified',
                        'sq.radiant', 'heart-modified', 'oval-modified', 'pear-modified',
                        'asscher', 'sq.emerald', 'baguette', 'european-cut', 'old miner',
                        'briolette', 'bullets', 'calf', 'circular-brilliant', 'epaulette',
                        'flanders', 'half-moon', 'hexagonal', 'kite', 'lozenge', 'octagonal',
                        'pentagonal', 'rose', 'shield', 'square', 'star', 'tapered-bagutte',
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant','Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='rap_date desc', limit=1)
                record.rap = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap = 0.00

    @api.depends('rap', 'avg_per_carat', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id', 'polish_id',
                 'symmetry_id', 'florescence_id')
    def _compute_avg_rap_back(self):
        for record in self:
            disc_percentage = ind_disc = dir_disc = 0.00
            if record.rap != 0 and record.avg_per_carat != 0:
                disc_percentage = (record.avg_per_carat / record.rap - 1) * 100
                record.avg_rap_back = disc_percentage + dir_disc + ind_disc
            else:
                record.avg_rap_back = 0.00

    @api.model
    def create(self, vals):
        # List of fields to check and their corresponding y_attribute_type
        attribute_field_mapping = {
            'size_id': 'size',
            'shape_id': 'shape',
            'colour_id': 'color',
            'clarity_id': 'clarity',
            'cut_id': 'cut',
            'polish_id': 'polish',
            'symmetry_id': 'sym',
            'florescence_id': 'florescence',
        }

        # Check each field in attribute_field_mapping
        for field, attribute_type in attribute_field_mapping.items():
            if field in vals:
                # Search for the corresponding attribute value
                attribute_value = self._get_active_attribute_value(vals[field], attribute_type)
                if not attribute_value:
                    raise ValidationError(f"The selected {field} is either inactive or incorrect.")
                # Update the field in the vals to ensure correct reference
                vals[field] = attribute_value.id

        # After checking, create the record
        return super(LessDiscountLine, self).create(vals)

    def _get_active_attribute_value(self, value_id, attribute_type):
        """Helper function to search and return active attribute values based on type."""
        return self.env['product.attribute.value'].search([
            ('id', '=', value_id),
            ('attribute_id.y_attribute_type', '=', attribute_type),
            ('attribute_id.y_status', '=', 'active')
        ], limit=1)