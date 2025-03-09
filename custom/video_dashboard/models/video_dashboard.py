# See LICENSE file for full copyright and licensing details.
import requests
import re
from odoo import api, fields, models, _


from odoo.exceptions import ValidationError
import datetime

class InventoryPricing(models.Model):
    _name = 'video.dashboard'
    _description = 'video dashboard'

    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New', tracking=True)
    inventory_pricing_id = fields.Many2one(
        "inventory.pricing",  # Model name of inventory_pricing
        string="Related Inventory",
        ondelete="cascade"
    )
    polish_codes = fields.Char(
        string="Item CD",
        related="inventory_pricing_id.polish_code",
        store=True
    )
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    certificate_no = fields.Char(string="Certificate No")
    cert_link = fields.Char(string="Cert_url")
    size =fields.Float(string="size")
    shape_name = fields.Char(string='Shape Name')  # Stores raw shape name
    colour = fields.Char(string="colour")
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    florescence_id = fields.Many2one('product.attribute.value', string='Florescence')
    image_id = fields.Image(string="Face Up Image", attachment=False, max_width=256, max_height=56)
    video_id = fields.Binary(string="3D Video", attachment=True)
    tweezer_video =fields.Binary(string="Tweezer_Video",attachment=True)
    on_hand_video = fields.Binary(string="On_Hand_Video", attachment=True)
    front_and_back_video = fields.Binary(string="Front_And_Back_Video", attachment=True)
    on_box_video = fields.Binary(string="On_Box_Video", attachment=True)
    shadecard_video = fields.Binary(string="Shadecard_Video", attachment=True)

    @api.onchange('inventory_pricing_id')
    def _onchange_inventory_pricing(self):
        if self.inventory_pricing_id:
            self.certificate_no = self.inventory_pricing_id.certificate_no
            self.cert_link = self.inventory_pricing_id.cert_link
            self.size = self.inventory_pricing_id.size
            self.shape_name = self.inventory_pricing_id.shape_name
            self.colour = self.inventory_pricing_id.colour
            self.clarity_id = self.inventory_pricing_id.clarity_id.id
            self.cut_id = self.inventory_pricing_id.cut_id.id
            self.florescence_id = self.inventory_pricing_id.florescence_id.id
        else:
            # Reset fields if no inventory_pricing is selected
            self.certificate_no = False
            self.cert_link = False
            self.size = False
            self.shape_name = False
            self.colour = False
            self.clarity_id = False
            self.cut_id = False
            self.florescence_id = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('inventory.pricing') or 'New'
        return super(InventoryPricing, self).create(vals)


