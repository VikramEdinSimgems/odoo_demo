# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


# plm/models/discount_indirect.py
from datetime import date

class PricingPlanning(models.TransientModel):
    _name = 'pricing.planning'
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']
    _description = 'Pricing Planning'


    date = fields.Date('Date')
    user_id = fields.Many2one('res.users',string='Created By')
    create_date = fields.Date('Created date')
    pricing_id = fields.Many2one('pricing.engine',string="Pricing Engine")
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
    clarity_id = fields.Many2one('product.attribute.value',string='Clarity')
    florescence_id = fields.Many2one('product.attribute.value',string='Florescense')
    shade_id = fields.Many2one('product.attribute.value',string='Shade')
    colour_id = fields.Many2one('product.attribute.value',string='Colour')
    cut_id = fields.Many2one('product.attribute.value',string='Cut')
    polish_id = fields.Many2one('product.attribute.value',string='Polish')
    size_id = fields.Many2one('product.attribute.value',string='Size')
    symmetry_id = fields.Many2one('product.attribute.value',string='Symmetry')
    luster_id = fields.Many2one('product.attribute.value',string='Luster')
    heart_arrow_id = fields.Many2one('product.attribute.value',string='H&A')
    diamond_type_id = fields.Many2one('product.attribute.value',string='DT')
    icon_id = fields.Many2one('ir.attachment', string='Shape', 
                              domain="[('res_model', '=', 'pricing.engine'), ('res_field', '=', 'icon_id')]")
    shape_id = fields.Many2one('product.attribute.value',string='Shape')
    remarks = fields.Text('Remarks')


    @api.onchange('icon_id')
    def _onchange_icon(self):
        for data in self:
            if data.icon_id:
                if data.icon_id.name.split('.')[0] == 'round':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Round')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'pear':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Pear')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'emerald':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Emerald')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'radiant':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Radiant')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'oval':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Oval')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'Cu_modified':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Cushion-Modified')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'Cu_brilliant':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Cushion-Brilliant')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'princess':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Princess')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'heart':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Heart')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'sq_emerald':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'SQ.Emerald')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'marquise':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Marquise')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'asscher':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Asscher')], limit=1).id
                if data.icon_id.name.split('.')[0] == 'Others':
                    data.shape_id = self.env['product.attribute.value'].search(
                        [('name', '=', 'Other')], limit=1).id


    def confirm_action(self):
        for record in self:
            # Create a new line item in the main model
            if record.pricing_id and record.plan == "plan_1":
                self.env['pricing.engine.line1'].create({
                    'pricing_id': record.pricing_id.id,
                    'plan': record.plan,
                    'size_id': record.size_id.id,
                    'colour_id': record.colour_id.id,
                    'clarity_id': record.clarity_id.id,
                    'cut_id': record.cut_id.id,
                    'polish_id': record.polish_id.id,
                    'symmetry_id': record.symmetry_id.id,
                    'florescence_id': record.florescence_id.id,
                    'shade_id': record.shade_id.id,
                    'shape_id': record.shape_id.id,
                    'luster_id': record.luster_id.id,
                    'heart_arrow_id': record.heart_arrow_id.id,
                    'diamond_type_id': record.diamond_type_id.id,
                    'combination': record.combination,
                })
            if record.pricing_id and record.plan == "plan_2":
                self.env['pricing.engine.line2'].create({
                    'pricing_id': record.pricing_id.id,
                    'plan': record.plan,
                    'size_id': record.size_id.id,
                    'colour_id': record.colour_id.id,
                    'clarity_id': record.clarity_id.id,
                    'cut_id': record.cut_id.id,
                    'polish_id': record.polish_id.id,
                    'symmetry_id': record.symmetry_id.id,
                    'florescence_id': record.florescence_id.id,
                    'shade_id': record.shade_id.id,
                    'shape_id': record.shape_id.id,
                    'luster_id': record.luster_id.id,
                    'heart_arrow_id': record.heart_arrow_id.id,
                    'diamond_type_id': record.diamond_type_id.id,
                    'combination': record.combination,
                })
            if record.pricing_id and record.plan == "plan_3":
                self.env['pricing.engine.line3'].create({
                    'pricing_id': record.pricing_id.id,
                    'plan': record.plan,
                    'size_id': record.size_id.id,
                    'colour_id': record.colour_id.id,
                    'clarity_id': record.clarity_id.id,
                    'cut_id': record.cut_id.id,
                    'polish_id': record.polish_id.id,
                    'symmetry_id': record.symmetry_id.id,
                    'florescence_id': record.florescence_id.id,
                    'shade_id': record.shade_id.id,
                    'shape_id': record.shape_id.id,
                    'luster_id': record.luster_id.id,
                    'heart_arrow_id': record.heart_arrow_id.id,
                    'diamond_type_id': record.diamond_type_id.id,
                    'combination': record.combination,
                })
            if record.pricing_id and record.plan == "plan_4":
                self.env['pricing.engine.line4'].create({
                    'pricing_id': record.pricing_id.id,
                    'plan': record.plan,
                    'size_id': record.size_id.id,
                    'colour_id': record.colour_id.id,
                    'clarity_id': record.clarity_id.id,
                    'cut_id': record.cut_id.id,
                    'polish_id': record.polish_id.id,
                    'symmetry_id': record.symmetry_id.id,
                    'florescence_id': record.florescence_id.id,
                    'shade_id': record.shade_id.id,
                    'shape_id': record.shape_id.id,
                    'luster_id': record.luster_id.id,
                    'heart_arrow_id': record.heart_arrow_id.id,
                    'diamond_type_id': record.diamond_type_id.id,
                    'combination': record.combination,
                })
            if record.pricing_id and record.plan == "plan_5":
                    self.env['pricing.engine.line5'].create({
                        'pricing_id': record.pricing_id.id,
                        'plan': record.plan,
                        'size_id': record.size_id.id,
                        'colour_id': record.colour_id.id,
                        'clarity_id': record.clarity_id.id,
                        'cut_id': record.cut_id.id,
                        'polish_id': record.polish_id.id,
                        'symmetry_id': record.symmetry_id.id,
                        'florescence_id': record.florescence_id.id,
                        'shade_id': record.shade_id.id,
                        'shape_id': record.shape_id.id,
                        'luster_id': record.luster_id.id,
                        'heart_arrow_id': record.heart_arrow_id.id,
                        'diamond_type_id': record.diamond_type_id.id,
                        'combination': record.combination,
                    })
            if record.pricing_id and record.plan == "plan_6":
                    self.env['pricing.engine.line6'].create({
                        'pricing_id': record.pricing_id.id,
                        'plan': record.plan,
                        'size_id': record.size_id.id,
                        'colour_id': record.colour_id.id,
                        'clarity_id': record.clarity_id.id,
                        'cut_id': record.cut_id.id,
                        'polish_id': record.polish_id.id,
                        'symmetry_id': record.symmetry_id.id,
                        'florescence_id': record.florescence_id.id,
                        'shade_id': record.shade_id.id,
                        'shape_id': record.shape_id.id,
                        'luster_id': record.luster_id.id,
                        'heart_arrow_id': record.heart_arrow_id.id,
                        'diamond_type_id': record.diamond_type_id.id,
                        'combination': record.combination,
                    })
            if record.pricing_id and record.plan == "plan_7":
                    self.env['pricing.engine.line7'].create({
                        'pricing_id': record.pricing_id.id,
                        'plan': record.plan,
                        'size_id': record.size_id.id,
                        'colour_id': record.colour_id.id,
                        'clarity_id': record.clarity_id.id,
                        'cut_id': record.cut_id.id,
                        'polish_id': record.polish_id.id,
                        'symmetry_id': record.symmetry_id.id,
                        'florescence_id': record.florescence_id.id,
                        'shade_id': record.shade_id.id,
                        'shape_id': record.shape_id.id,
                        'luster_id': record.luster_id.id,
                        'heart_arrow_id': record.heart_arrow_id.id,
                        'diamond_type_id': record.diamond_type_id.id,
                        'combination': record.combination,
                    })
            if record.pricing_id and record.plan == "plan_8":
                    self.env['pricing.engine.line8'].create({
                        'pricing_id': record.pricing_id.id,
                        'plan': record.plan,
                        'size_id': record.size_id.id,
                        'colour_id': record.colour_id.id,
                        'clarity_id': record.clarity_id.id,
                        'cut_id': record.cut_id.id,
                        'polish_id': record.polish_id.id,
                        'symmetry_id': record.symmetry_id.id,
                        'florescence_id': record.florescence_id.id,
                        'shade_id': record.shade_id.id,
                        'shape_id': record.shape_id.id,
                        'luster_id': record.luster_id.id,
                        'heart_arrow_id': record.heart_arrow_id.id,
                        'diamond_type_id': record.diamond_type_id.id,
                        'combination': record.combination,
                    })
            if record.pricing_id and record.plan == "plan_9":
                    self.env['pricing.engine.line9'].create({
                        'pricing_id': record.pricing_id.id,
                        'plan': record.plan,
                        'size_id': record.size_id.id,
                        'colour_id': record.colour_id.id,
                        'clarity_id': record.clarity_id.id,
                        'cut_id': record.cut_id.id,
                        'polish_id': record.polish_id.id,
                        'symmetry_id': record.symmetry_id.id,
                        'florescence_id': record.florescence_id.id,
                        'shade_id': record.shade_id.id,
                        'shape_id': record.shape_id.id,
                        'luster_id': record.luster_id.id,
                        'heart_arrow_id': record.heart_arrow_id.id,
                        'diamond_type_id': record.diamond_type_id.id,
                        'combination': record.combination,
                    })
            if record.pricing_id and record.plan == "plan_10":
                    self.env['pricing.engine.line10'].create({
                        'pricing_id': record.pricing_id.id,
                        'plan': record.plan,
                        'size_id': record.size_id.id,
                        'colour_id': record.colour_id.id,
                        'clarity_id': record.clarity_id.id,
                        'cut_id': record.cut_id.id,
                        'polish_id': record.polish_id.id,
                        'symmetry_id': record.symmetry_id.id,
                        'florescence_id': record.florescence_id.id,
                        'shade_id': record.shade_id.id,
                        'shape_id': record.shape_id.id,
                        'luster_id': record.luster_id.id,
                        'heart_arrow_id': record.heart_arrow_id.id,
                        'diamond_type_id': record.diamond_type_id.id,
                        'combination': record.combination,
                    })
        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}