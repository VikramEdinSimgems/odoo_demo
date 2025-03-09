# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
# plm/models/plm_weightage.py

class PlmWeightage(models.Model):
    _name = 'plm.weightage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PLM Weightage'


    name = fields.Char(string="Name", required=True)
    weightage = fields.Float(string="Weightage", required=True)



    @api.constrains('weightage')
    def _check_weightage(self):
        for data in self:
            if data.weightage < 0 and data.weightage < 100:
                raise ValidationError(
                    "You can only enter the weightage value between 0 - 100."
                )