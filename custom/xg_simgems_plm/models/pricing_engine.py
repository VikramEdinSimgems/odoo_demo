# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from datetime import date

from reportlab.lib.pdfencrypt import computeO


class PricingEngine(models.Model):
    _name = 'pricing.engine'
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']
    _description = 'Pricing Engine'


    name = fields.Char(string='Sequence', required=True, copy=False, default='New',tracking=True)    
    sequence_no = fields.Char(string='Sequence No', readonly=True, required=True, copy=False, default='New',tracking=True)
    date = fields.Date('Date',tracking=True)
    plan_no = fields.Char('Plan No')
    user_id = fields.Many2one('res.users',string='Created By',tracking=True)
    approved_user_id = fields.Many2one('res.users', string='Approved By', tracking=True, readonly=True)
    approved_date = fields.Date(string='Approved Date', tracking=True, readonly=True)
    create_date = fields.Date('Created date',tracking=True)
    rough_weight = fields.Float('Rough Weight',tracking=True)
    # discount_id = fields.Many2one('')
    rap_id = fields.Many2one('rap.price',tracking=True)
    less_discount_id = fields.Many2one('less.discount','Less Discount base',tracking=True)
    plan = fields.Selection([('plan_1','Plan 1'),('plan_2','Plan 2'),('plan_3','Plan 3'),('plan_4','Plan 4'),('plan_5','Plan 5'),('plan_6','Plan 6'),('plan_7','Plan 7'),
                             ('plan_8','Plan 8'),('plan_9','Plan 9'),('plan_10','Plan 10')],string='Plan',)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft',tracking=True)

    line_items_1 = fields.One2many('pricing.engine.line1', 'pricing_id', string='Plan 1',copy=True)
    line_items_2 = fields.One2many('pricing.engine.line2', 'pricing_id', string='Plan 2',copy=True)
    line_items_3 = fields.One2many('pricing.engine.line3', 'pricing_id', string='Plan 3',copy=True)
    line_items_4 = fields.One2many('pricing.engine.line4', 'pricing_id', string='Plan 4',copy=True)
    line_items_5 = fields.One2many('pricing.engine.line5', 'pricing_id', string='Plan 5',copy=True)
    line_items_6 = fields.One2many('pricing.engine.line6', 'pricing_id', string='Plan 6',copy=True)
    line_items_7 = fields.One2many('pricing.engine.line7', 'pricing_id', string='Plan 7',copy=True)
    line_items_8 = fields.One2many('pricing.engine.line8', 'pricing_id', string='Plan 8',copy=True)
    line_items_9 = fields.One2many('pricing.engine.line9', 'pricing_id', string='Plan 9',copy=True)
    line_items_10 = fields.One2many('pricing.engine.line10', 'pricing_id', string='Plan 10',copy=True)

    hide_button = fields.Boolean(string='Hide Button',default=False,copy=False)

    plan_total_amount_1 = fields.Float(compute='_compute_total')
    plan_total_amount_2 = fields.Float(compute='_compute_total')
    plan_total_amount_3 = fields.Float(compute='_compute_total')
    plan_total_amount_4 = fields.Float(compute='_compute_total')
    plan_total_amount_5 = fields.Float(compute='_compute_total')
    plan_total_amount_6 = fields.Float(compute='_compute_total')
    plan_total_amount_7 = fields.Float(compute='_compute_total')
    plan_total_amount_8 = fields.Float(compute='_compute_total')
    plan_total_amount_9 = fields.Float(compute='_compute_total')
    plan_total_amount_10 = fields.Float(compute='_compute_total')

    is_plan_1_highest = fields.Boolean('Is Plan 1 Top?',readonly=True,copy=False,store=True)
    is_plan_2_highest = fields.Boolean('Is Plan 2 Top?',readonly=True,copy=False,store=True)
    is_plan_3_highest = fields.Boolean('Is Plan 3 Top?',readonly=True,copy=False,store=True)
    is_plan_4_highest = fields.Boolean('Is Plan 4 Top?',readonly=True,copy=False,store=True)
    is_plan_5_highest = fields.Boolean('Is Plan 5 Top?',readonly=True,copy=False,store=True)
    is_plan_6_highest = fields.Boolean('Is Plan 6 Top?',readonly=True,copy=False,store=True)
    is_plan_7_highest = fields.Boolean('Is Plan 7 Top?',readonly=True,copy=False,store=True)
    is_plan_8_highest = fields.Boolean('Is Plan 8 Top?',readonly=True,copy=False,store=True)
    is_plan_9_highest = fields.Boolean('Is Plan 9 Top?',readonly=True,copy=False,store=True)
    is_plan_10_highest = fields.Boolean('Is Plan 10 Top?',readonly=True,copy=False,store=True)


    @api.depends('line_items_1','line_items_2','line_items_3','line_items_4','line_items_5','line_items_6','line_items_7','line_items_8','line_items_9','line_items_10')
    def _compute_total(self):
        for data in self:
            data.plan_total_amount_1 = sum(line.total_price for line in data.line_items_1) if data.line_items_1 else 0
            data.plan_total_amount_2 = sum(line.total_price for line in data.line_items_2) if data.line_items_2 else 0
            data.plan_total_amount_3 = sum(line.total_price for line in data.line_items_3) if data.line_items_3 else 0
            data.plan_total_amount_4 = sum(line.total_price for line in data.line_items_4) if data.line_items_4 else 0
            data.plan_total_amount_5 = sum(line.total_price for line in data.line_items_5) if data.line_items_5 else 0
            data.plan_total_amount_6 = sum(line.total_price for line in data.line_items_6) if data.line_items_6 else 0
            data.plan_total_amount_7 = sum(line.total_price for line in data.line_items_7) if data.line_items_7 else 0
            data.plan_total_amount_8 = sum(line.total_price for line in data.line_items_8) if data.line_items_8 else 0
            data.plan_total_amount_9 = sum(line.total_price for line in data.line_items_9) if data.line_items_9 else 0
            data.plan_total_amount_10 = sum(line.total_price for line in data.line_items_10) if data.line_items_10 else 0

    @api.model
    def create(self, vals):
        # Ensure the 'name' field gets a sequence value if it's set to 'New' or not provided.
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pricing.engine') or 'New'
        # Set the current date if 'date' is not provided
        if 'date' not in vals:
            vals['date'] = fields.Date.today()
        # Create the record using the parent class's create method
        record = super(PricingEngine, self).create(vals)
        # Post a message on the chatter about the creation
        record.message_post(
            body=f"Record {record.name} created by user: {self.env.user.name}",
            subtype_id=self.env.ref('mail.mt_note').id,  # Ensure the subtype reference exists
        )
        return record

    def action_request(self):
        for data in self:
            data.state = 'requested'
            data.message_post(
                body=f"Record {data.name} requested for approval by user: {self.env.user.name}",
                subtype_id=self.env.ref('mail.mt_note').id,  # Ensure the subtype reference exists
            )
    def action_approve(self):
        for data in self:
            is_any_item_approved = any(
                line.approval_status == 'approved'
                for line_items in [
                    data.line_items_1,
                    data.line_items_2,
                    data.line_items_3,
                    data.line_items_4,
                    data.line_items_5,
                    data.line_items_6,
                    data.line_items_7,
                    data.line_items_8,
                    data.line_items_9,
                    data.line_items_10,
                ]
                for line in line_items
            )
            if not is_any_item_approved:
                raise  ValidationError("Approval cannot proceed because no plan is in the 'approved' state.")
            data.state = 'approved'
            data.message_post(
                body=f"Record {data.name} approved by user: {self.env.user.name}",
                subtype_id=self.env.ref('mail.mt_note').id,  # Ensure the subtype reference exists
            )

    def action_cancel(self):
        for data in self:
            data.state = 'cancel'
            data.message_post(
                body=f"Record {data.name} approved by user: {self.env.user.name}",
                subtype_id=self.env.ref('mail.mt_note').id,  # Ensure the subtype reference exists
            )

    def action_reject(self):
        for data in self:
            data.state = 'rejected'
            data.hide_button = False
            data.is_plan_1_highest = False
            data.is_plan_2_highest = False
            data.is_plan_3_highest = False
            data.is_plan_4_highest = False
            data.is_plan_5_highest = False
            data.is_plan_6_highest = False
            data.is_plan_7_highest = False
            data.is_plan_8_highest = False
            data.is_plan_9_highest = False
            data.is_plan_10_highest = False
            for line_items in [data.line_items_1, data.line_items_2,data.line_items_3, data.line_items_4, data.line_items_5, data.line_items_6, data.line_items_7,
                               data.line_items_8, data.line_items_9, data.line_items_10]:
                if line_items:
                    for line in line_items:
                        line.approval_status = 'draft'
            data.message_post(
                body=f"Record {data.name} rejected by user: {self.env.user.name}",
                subtype_id=self.env.ref('mail.mt_note').id,  # Ensure the subtype reference exists
            )

    def action_done(self):
        for data in self:
            # data.state = 'done'
            data._compute_which_plan_is_highest()


    def action_reset_to_draft(self):
        for data in self:
            data.state = 'draft'
            data.hide_button = False
            data.is_plan_1_highest = False
            data.is_plan_2_highest = False
            data.is_plan_3_highest = False
            data.is_plan_4_highest = False
            data.is_plan_5_highest = False
            data.is_plan_6_highest = False
            data.is_plan_7_highest = False
            data.is_plan_8_highest = False
            data.is_plan_9_highest = False
            data.is_plan_10_highest = False
            for line_items in [data.line_items_1, data.line_items_2,data.line_items_3, data.line_items_4, data.line_items_5, data.line_items_6, data.line_items_7,
                               data.line_items_8, data.line_items_9, data.line_items_10]:
                if line_items:
                    for line in line_items:
                        line.approval_status = 'draft'
            data.message_post(
                body=f"Record {data.name} reset to draft by user: {self.env.user.name}",
                subtype_id=self.env.ref('mail.mt_note').id,  # Ensure the subtype reference exists
            )

    #Button Action for add line items
    def open_pricing_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pricing Planning',
            'res_model': 'pricing.planning',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_pricing_id': self.id,
                        'default_plan': self.plan,
                        },
        }

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6', 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_1(self):
        # Approve all items in line_items_1
        for line in self.line_items_1:
            line.approval_status = 'approved'
        self.is_plan_1_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_2, self.line_items_3, self.line_items_4, self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_8, self.line_items_9, self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6', 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_2(self):
        # Approve all items in line_items_2
        for line in self.line_items_2:
            line.approval_status = 'approved'
        self.is_plan_2_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_3, self.line_items_4, self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_8, self.line_items_9, self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6', 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_3(self):
        # Approve all items in line_items_3
        for line in self.line_items_3:
            line.approval_status = 'approved'
        self.is_plan_3_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_4, self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_8, self.line_items_9, self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6', 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_4(self):
        # Approve all items in line_items_4
        for line in self.line_items_4:
            line.approval_status = 'approved'
        self.is_plan_4_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_8, self.line_items_9, self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6', 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_5(self):
        # Approve all items in line_items_5
        for line in self.line_items_5:
            line.approval_status = 'approved'
        self.is_plan_5_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_4, self.line_items_6, self.line_items_7, self.line_items_8, self.line_items_9, self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6',
                 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_6(self):
        # Approve all items in line_items_6
        for line in self.line_items_6:
            line.approval_status = 'approved'
        self.is_plan_6_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_4,
                           self.line_items_5, self.line_items_7, self.line_items_8, self.line_items_9,
                           self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6',
                 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_7(self):
        # Approve all items in line_items_7
        for line in self.line_items_7:
            line.approval_status = 'approved'
        self.is_plan_7_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_4,
                           self.line_items_5, self.line_items_6, self.line_items_8, self.line_items_9,
                           self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6',
                 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_8(self):
        # Approve all items in line_items_8
        for line in self.line_items_8:
            line.approval_status = 'approved'
        self.is_plan_8_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_4,
                           self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_9,
                           self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6',
                 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_9(self):
        # Approve all items in line_items_9
        for line in self.line_items_9:
            line.approval_status = 'approved'
        self.is_plan_9_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_4,
                           self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_8,
                           self.line_items_10]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

    @api.depends('line_items_1', 'line_items_2', 'line_items_3', 'line_items_4', 'line_items_5', 'line_items_6',
                 'line_items_7', 'line_items_8', 'line_items_9', 'line_items_10')
    def action_approve_items_10(self):
        # Approve all items in line_items_10
        for line in self.line_items_10:
            line.approval_status = 'approved'
        self.is_plan_10_highest = True
        # Reject items in all other line_items lists
        for line_items in [self.line_items_1, self.line_items_2, self.line_items_3, self.line_items_4,
                           self.line_items_5, self.line_items_6, self.line_items_7, self.line_items_8,
                           self.line_items_9]:
            if line_items:
                for line in line_items:
                    line.approval_status = 'rejected'
        self.hide_button = True

class PricingEngineLine1(models.Model):
    _name = 'pricing.engine.line1'
    _description = 'Pricing Engine Line1'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1','Plan 1'),
                             ('plan_2','Plan 2'),
                             ('plan_3','Plan 3'),
                             ('plan_4','Plan 4'),
                             ('plan_5','Plan 5'),
                             ('plan_6','Plan 6'),
                             ('plan_7','Plan 7'),
                             ('plan_8','Plan 8'),
                             ('plan_9','Plan 9'),
                             ('plan_10','Plan 10')],
                             string='Plan')
    combination = fields.Selection([('comb_1','Combination 1'),
                             ('comb_2','Combination 2'),
                             ('comb_3','Combination 3'),
                             ('comb_4','Combination 4'),
                             ('comb_5','Combination 5'),
                             ('comb_6','Combination 6'),
                             ('comb_7','Combination 7'),
                             ('comb_8','Combination 8'),
                             ('comb_9','Combination 9'),
                             ('comb_10','Combination 10')],
                             string='Combination')
    approval_status = fields.Selection([('draft','Draft'),('approved','Approved'),('rejected','Rejected')],default='draft',string='Approval Status')
    size_id = fields.Many2one('product.attribute.value',string='Size')
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    cut_id = fields.Many2one('product.attribute.value',string='Cut')
    polish_id = fields.Many2one('product.attribute.value',string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value',string='Sym')
    florescence_id = fields.Many2one('product.attribute.value',string='Flo')
    luster_id = fields.Many2one('product.attribute.value',string='Luster')
    shade_id = fields.Many2one('product.attribute.value',string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value',string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value',string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back',compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat',compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price',compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat',compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price',compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(data.size_id.name)) if data.price_per_carat and data.size_id else 0.00


    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))
                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id,record.colour_id, record.clarity_id,record.cut_id,record.polish_id,record.symmetry_id,record.florescence_id]):
                # Build the domain for the base price
                domain=[
                        ('size_id', '=', record.size_id.id),
                        ('colour_id', '=', record.colour_id.id),
                        ('clarity_id', '=', record.clarity_id.id),
                        ('shape_id', '=', record.shape_id.id),
                        ('cut_id', '=', record.cut_id.id),
                        ('polish_id', '=', record.polish_id.id),
                        ('symmetry_id', '=', record.symmetry_id.id),
                        ('florescence_id', '=', record.florescence_id.id),
                        # ('rap_id.state', '=', 'approved')
                    ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat','rap_price','size_id','shape_id','colour_id','clarity_id','cut_id','polish_id','symmetry_id','florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount/100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain,order='approved_date desc', limit=1)
                    dir_disc = (dir_disc_line.discount/100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat/data.rap_price-1)*100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat/data.rap_price-1)*100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00





class PricingEngineLine2(models.Model):
    _name = 'pricing.engine.line2'
    _description = 'Pricing Engine Line2'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00


class PricingEngineLine3(models.Model):
    _name = 'pricing.engine.line3'
    _description = 'Pricing Engine Line3'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
                domain = [
                    ('from_size_id.y_sequence_no', '<=', size_sequence),
                    ('to_size_id.y_sequence_no', '>=', size_sequence),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('rap_id.state', '=', 'approved')
                ]

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00


class PricingEngineLine4(models.Model):
    _name = 'pricing.engine.line4'
    _description = 'Pricing Engine Line4'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00

class PricingEngineLine5(models.Model):
    _name = 'pricing.engine.line5'
    _description = 'Pricing Engine Line5'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00

class PricingEngineLine6(models.Model):
    _name = 'pricing.engine.line6'
    _description = 'Pricing Engine Line6'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))
                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00

class PricingEngineLine7(models.Model):
    _name = 'pricing.engine.line7'
    _description = 'Pricing Engine Line7'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00

class PricingEngineLine8(models.Model):
    _name = 'pricing.engine.line8'
    _description = 'Pricing Engine Line8'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00

class PricingEngineLine9(models.Model):
    _name = 'pricing.engine.line9'
    _description = 'Pricing Engine Line9'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00


class PricingEngineLine10(models.Model):
    _name = 'pricing.engine.line10'
    _description = 'Pricing Engine Line10'

    pricing_id = fields.Many2one('pricing.engine', string='Pricing Engine', ondelete='cascade')
    plan = fields.Selection([('plan_1', 'Plan 1'),
                             ('plan_2', 'Plan 2'),
                             ('plan_3', 'Plan 3'),
                             ('plan_4', 'Plan 4'),
                             ('plan_5', 'Plan 5'),
                             ('plan_6', 'Plan 6'),
                             ('plan_7', 'Plan 7'),
                             ('plan_8', 'Plan 8'),
                             ('plan_9', 'Plan 9'),
                             ('plan_10', 'Plan 10')],
                            string='Plan')
    combination = fields.Selection([('comb_1', 'Combination 1'),
                                    ('comb_2', 'Combination 2'),
                                    ('comb_3', 'Combination 3'),
                                    ('comb_4', 'Combination 4'),
                                    ('comb_5', 'Combination 5'),
                                    ('comb_6', 'Combination 6'),
                                    ('comb_7', 'Combination 7'),
                                    ('comb_8', 'Combination 8'),
                                    ('comb_9', 'Combination 9'),
                                    ('comb_10', 'Combination 10')],
                                   string='Combination')
    approval_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='draft',
                                       string='Approval Status')
    size_id = fields.Many2one('product.attribute.value', string='Size')
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Flo')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_arrow_id = fields.Many2one('product.attribute.value', string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value', string='DT')
    remarks = fields.Text('Remarks')
    rate_sales = fields.Float('Rate-Sales')
    avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    total_price = fields.Float('Total Price', compute="_compute_total_price")

    def _compute_total_price(self):
        for data in self:
            data.total_price = (data.price_per_carat * float(
                data.size_id.name)) if data.price_per_carat and data.size_id else 0.00

    _sql_constraints = [
        ('unique_plan_combination',
         'UNIQUE(plan, combination, pricing_id)',
         'The combination of Plan and Combination must be unique per Pricing Engine.')
    ]

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_rap_price(self):
        for record in self:
            if all([record.size_id, record.colour_id, record.clarity_id]):
                size_sequence = record.size_id.y_sequence_no  # Get the sequence number of the current size_id
                # Build the domain for the base price
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
                        'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
                    ]
                    domain.append(('shape_id.name', 'in', fancy_shapes))

                rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
                record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
            else:
                record.rap_price = 0.00

    @api.depends('size_id', 'colour_id', 'clarity_id')
    def _compute_avg_rap_back(self):
        for record in self:
            if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id,
                    record.polish_id, record.symmetry_id, record.florescence_id]):
                # Build the domain for the base price
                domain = [
                    ('size_id', '=', record.size_id.id),
                    ('colour_id', '=', record.colour_id.id),
                    ('clarity_id', '=', record.clarity_id.id),
                    ('shape_id', '=', record.shape_id.id),
                    ('cut_id', '=', record.cut_id.id),
                    ('polish_id', '=', record.polish_id.id),
                    ('symmetry_id', '=', record.symmetry_id.id),
                    ('florescence_id', '=', record.florescence_id.id),
                    # ('rap_id.state', '=', 'approved')
                ]
                avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
                record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
                record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
            else:
                record.avg_rap_back = 0.00
                record.avg_price_per_carat = 0.00

    @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id',
                 'polish_id', 'symmetry_id', 'florescence_id')
    def _compute_price_carat(self):
        for data in self:
            dir_disc = ind_disc = 0
            if data.avg_price_per_carat != 0 and data.rap_price != 0:
                if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id,
                        data.symmetry_id, data.florescence_id]):
                    size_sequence = data.size_id.y_sequence_no  # Get the sequence number of the current size_id
                    shape_sequence = data.shape_id.y_sequence_no  # Get the sequence number of the current shape_id
                    colour_sequence = data.colour_id.y_sequence_no  # Get the sequence number of the current colour_id
                    clarity_sequence = data.clarity_id.y_sequence_no  # Get the sequence number of the current clarity_id
                    cut_sequence = data.cut_id.y_sequence_no  # Get the sequence number of the current cut_id
                    polish_sequence = data.polish_id.y_sequence_no  # Get the sequence number of the current polish_id
                    symmetry_sequence = data.symmetry_id.y_sequence_no  # Get the sequence number of the current symmetry_id
                    flor_sequence = data.florescence_id.y_sequence_no  # Get the sequence number of the current florescence_id
                    indirect_domain = [
                        ('from_size_id.y_sequence_no', '<=', size_sequence),
                        ('to_size_id.y_sequence_no', '>=', size_sequence),
                        ('from_shape_id.y_sequence_no', '<=', shape_sequence),
                        ('to_shape_id.y_sequence_no', '>=', shape_sequence),
                        ('from_clr_id.y_sequence_no', '<=', colour_sequence),
                        ('to_clr_id.y_sequence_no', '>=', colour_sequence),
                        ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
                        ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('discount_indirect_id.state', '=', 'approved'),
                    ]

                    ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain,
                                                                                  order='approved_date desc', limit=1)
                    ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
                    direct_domain = [
                        ('size_from_id.y_sequence_no', '<=', size_sequence),
                        ('size_to_id.y_sequence_no', '>=', size_sequence),
                        ('shape_id', '=', data.shape_id.id),
                        ('colour_id', '=', data.colour_id.id),
                        ('clarity_id', '=', data.clarity_id.id),
                        ('from_cut_id.y_sequence_no', '<=', cut_sequence),
                        ('to_cut_id.y_sequence_no', '>=', cut_sequence),
                        ('from_pol_id.y_sequence_no', '<=', polish_sequence),
                        ('to_pol_id.y_sequence_no', '>=', polish_sequence),
                        ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
                        ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
                        ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
                        ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
                        ('discount_direct_id.state', '=', 'approved'),
                    ]
                    dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc',
                                                                            limit=1)
                    dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
                    data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (
                                data.avg_price_per_carat * ind_disc)
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
                else:
                    data.price_per_carat = data.avg_rap_back
                    data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
            else:
                data.price_per_carat = 0.00
                data.final_rap_back = 0.00