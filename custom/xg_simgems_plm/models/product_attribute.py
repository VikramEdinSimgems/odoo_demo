# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    

    y_attribute_type = fields.Selection(
        [('carat','Carat'),('color','Colour'),('shape', 'Shape'), ('size', 'Size'), ('clarity', 'Clarity'),
         ('cut', 'Cut'), ('polish', 'PL'), ('sym', 'Sym'),
         ('florescence', 'FL'), ('bt', 'BT'), ('bc', 'BC'),
         ('wt', 'WT'), ('wc', 'WC'), ('shade', 'Shade'),
         ('ha', 'H&A'), ('ec', 'EC'), ('ls', 'Luster'),
         ('lab', 'LAB'), ('dt', 'DT')],
        string="Attribute Type",
    )
    y_status = fields.Selection([('inactive','Inactive'),('active','Active')],string="Status", default='inactive')

    def action_active(self):
        for data in self:
            data.y_status = 'active'

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    
    _sql_constraints = [
        ('unique_y_sequence_per_attribute', 
         'unique(attribute_id, y_sequence_no)', 
         'The sequence must be unique per attribute.')
    ]

    @api.depends('attribute_id')
    @api.depends_context('show_attribute')
    def _compute_display_name(self):
        """Override because in general the name of the value is confusing if it
        is displayed without the name of the corresponding attribute.
        Eg. on product list & kanban views, on BOM form view

        However during variant set up (on the product template form) the name of
        the attribute is already on each line so there is no need to repeat it
        on every value.
        """
        if not self.env.context.get('show_attribute', True):
            return super()._compute_display_name()
        for value in self:
            # Remove 'first name-' if it exists in value.name
            clean_name = value.name
            if clean_name:
                clean_name = clean_name.replace("Pol-", "").replace("Sym-", "").replace("CL-", "").replace("FL-", "").replace("SH-", "").replace("EY-", "").replace("Lu-", "").replace("DT-", "").replace("CL-", "").replace("Cut-", "")
            # cl_clean_name = value.name.replace("CL-", "") if value.name and "CL-" in value.name else value.name
            # value.display_name = cl_clean_name
            # fl_clean_name = value.name.replace("FL-", "") if value.name and "FL-" in value.name else value.name
            # value.display_name = fl_clean_name
            # sym_clean_name = value.name.replace("Sym-", "") if value.name and "Sym-" in value.name else value.name
            # value.display_name = sym_clean_name
            # pol_clean_name = value.name.replace("Pol-", "") if value.name and "Pol-" in value.name else value.name
            # value.display_name = pol_clean_name
            # sh_clean_name = value.name.replace("SH-", "") if value.name and "SH-" in value.name else value.name
            # value.display_name = sh_clean_name
            # cut_clean_name = value.name.replace("Cut-", "") if value.name and "Cut-" in value.name else value.name
            # value.display_name = cut_clean_name
            # dt_clean_name = value.name.replace("DT-", "") if value.name and "DT-" in value.name else value.name
            # value.display_name = dt_clean_name
            # lu_clean_name = value.name.replace("Lu-", "") if value.name and "Lu-" in value.name else value.name
            # value.display_name = lu_clean_name
            # ey_clean_name = value.name.replace("EY-", "") if value.name and "EY-" in value.name else value.name
            value.display_name = clean_name

    @api.constrains('y_sequence_no')
    def _check_y_sequence_not_zero(self):
        for record in self:
            if record.y_sequence_no == 0:
                raise ValidationError("The sequence value cannot be 0. Please set a value greater than or less than 0.")

    y_sequence_no = fields.Integer('Sequence No',required=True)
    y_short_code = fields.Char(string="Short Code")