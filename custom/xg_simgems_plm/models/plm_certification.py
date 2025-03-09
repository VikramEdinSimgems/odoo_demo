# -*- coding: utf-8 -*-

from odoo import models, fields, api


# plm/models/discount_indirect.py
from datetime import date

class PlmCertification(models.Model):
    _name = 'plm.certification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PLM Certification'


    name = fields.Char(string="Name", required=True)
    certification_number = fields.Char(string="Certification Number", required=True)