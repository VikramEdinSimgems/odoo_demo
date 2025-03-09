# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
# plm/models/plm_weightage.py

class PlmCompetitor(models.Model):
    _name = 'plm.competitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PLM Competitor'


    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
