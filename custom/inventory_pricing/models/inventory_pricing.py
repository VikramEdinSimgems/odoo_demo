# See LICENSE file for full copyright and licensing details.
import requests
import re
from odoo import api, fields, models, _


from odoo.exceptions import ValidationError
import datetime

class InventoryPricing(models.Model):
    _name = 'inventory.pricing'
    _description = 'Inventory Pricing'
    _rec_name = "polish_code"

    name = fields.Char(string='Sequence', readonly=True, required=True, copy=False, default='New', tracking=True)
    polish_code = fields.Char(string="Item CD")
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    certificate_no = fields.Char(string="Certificate No")
    cert_link = fields.Char(string="Cert_url")
    size_id = fields.Many2one('product.attribute.value', string='Size')
    size =fields.Float(string="size")
    shape_name = fields.Char(string='Shape Name')  # Stores raw shape name
    shape_id = fields.Many2one('product.attribute.value', string='Shape')
    colour_id = fields.Many2one('product.attribute.value', string='Colour')
    colour = fields.Char(string="colour")
    clarity_id = fields.Many2one('product.attribute.value', string='Clarity')
    cut_id = fields.Many2one('product.attribute.value', string='Cut')
    polish_id = fields.Many2one('product.attribute.value', string='Pol')
    symmetry_id = fields.Many2one('product.attribute.value', string='Sym')
    florescence_id = fields.Many2one('product.attribute.value', string='Florescence')
    image_id = fields.Char(string="Image")
    video_id = fields.Char(string="video ")
    bt_id = fields.Many2one('product.attribute.value', string='Black Table Inclusion')
    bc_id = fields.Many2one('product.attribute.value', string='Black Crown Inclusion')
    wt_id = fields.Many2one('product.attribute.value', string='White Table Inclusion')
    wc_id = fields.Many2one('product.attribute.value', string='White Crown Inclusion')
    shade_id = fields.Many2one('product.attribute.value', string='Shade')
    heart_id = fields.Many2one('product.attribute.value', string='Heart & Arrow')
    ec_id = fields.Many2one('product.attribute.value', string='Eye clean')
    luster_id = fields.Many2one('product.attribute.value', string='Luster')
    lab_id = fields.Many2one('product.attribute.value', string='LAB')
    diamond_type_id = fields.Many2one('product.attribute.value', string='Diamond Type')
    cert_comments = fields.Text(string="Cert Comments")
    country = fields.Char(string="country")
    key_to_symbols = fields.Text(string="Key to Symbols")
    status = fields.Selection([
        ('available', 'Available'),
        ('memo', 'Memo'),
        ('hold', 'On Hold'),
    ], string="Status", default="available")
    stone_status=fields.Char(string="Status")
    ratio = fields.Float(string="Ratio")
    measurement = fields.Char(string="Measurement")
    table_perc = fields.Float(string="Table %")
    depth_perc = fields.Float(string="Depth %")
    crown_angle = fields.Float(string="Crown Angle")
    pavilion_angle = fields.Float(string="Pavilion Angle")
    pavilion_depth = fields.Float(string="Pavilion Depth")
    rap_price1 =fields.Float(string="rap_price")
    price_per_carat1=fields.Float(string="price_per_carat")
    final_rap_back1 = fields.Float(string="Final Rap Back 1", compute="_compute_final_rap_back", store=True)

    # calculation part
    # avg_rap_back = fields.Float('Avg Rap Back', compute='_compute_avg_rap_back')
    # avg_price_per_carat = fields.Float('Avg Price/Carat', compute='_compute_avg_rap_back')
    # rap_price = fields.Float('RAP Price', compute='_compute_rap_price')
    # price_per_carat = fields.Float('Price/Carat', compute='_compute_price_carat')
    # final_rap_back = fields.Float('Final Rap Back', compute='_compute_price_carat')
    # total_price = fields.Float('Total Price', compute="_compute_total_price")


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('inventory.pricing') or 'New'
        return super(InventoryPricing, self).create(vals)

    # def _compute_total_price(self):
    #     for data in self:
    #         try:
    #             size_value = float(data.size_id.name)
    #         except (ValueError, TypeError):
    #             size_value = 0.0
    #         data.total_price = (data.price_per_carat * size_value) if data.price_per_carat and data.size_id else 0.00

    # @api.depends('size_id', 'colour_id', 'clarity_id', 'shape_id')
    # def _compute_rap_price(self):
    #     for record in self:
    #         if all([record.size_id, record.colour_id, record.clarity_id]):
    #             size_sequence = record.size_id.y_sequence_no
    #             domain = [
    #                 ('from_size_id.y_sequence_no', '<=', size_sequence),
    #                 ('to_size_id.y_sequence_no', '>=', size_sequence),
    #                 ('colour_id', '=', record.colour_id.id),
    #                 ('clarity_id', '=', record.clarity_id.id),
    #                 ('rap_id.state', '=', 'approved')
    #             ]
    #             if record.shape_id.name == 'round':
    #                 domain.append(('shape_id', '=', record.shape_id.id))
    #             else:
    #                 fancy_shapes = [
    #                     'pear', 'emerald', 'princess', 'cushion', 'oval', 'heart', 'marquise',
    #                     'cushion-modified', 'cushion-brilliant', 'radiant', 'radiant-modified',
    #                     'sq.radiant', 'heart-modified', 'oval-modified', 'pear-modified',
    #                     'asscher', 'sq.emerald', 'baguette', 'european-cut', 'old miner',
    #                     'briolette', 'bullets', 'calf', 'circular-brilliant', 'epaulette',
    #                     'flanders', 'half-moon', 'hexagonal', 'kite', 'lozenge', 'octagonal',
    #                     'pentagonal', 'rose', 'shield', 'square', 'star', 'tapered-bagutte',
    #                     'tapered-bullet', 'trapeziod', 'triangular', 'trilliant', 'Fancy'
    #                 ]
    #                 domain.append(('shape_id.name', 'in', fancy_shapes))
    #             rap_price_line = self.env['rap.price.line'].search(domain, order='create_date desc', limit=1)
    #             record.rap_price = rap_price_line.rap_price if rap_price_line else 0.00
    #         else:
    #             record.rap_price = 0.00

    # @api.depends('size_id', 'colour_id', 'clarity_id', 'shape_id')
    # def _compute_avg_rap_back(self):
    #     for record in self:
    #         if all([record.size_id, record.shape_id, record.colour_id, record.clarity_id, record.cut_id, record.polish_id, record.symmetry_id, record.florescence_id]):
    #             domain = [
    #                 ('size_id', '=', record.size_id.id),
    #                 ('colour_id', '=', record.colour_id.id),
    #                 ('clarity_id', '=', record.clarity_id.id),
    #                 ('shape_id', '=', record.shape_id.id),
    #                 ('cut_id', '=', record.cut_id.id),
    #                 ('polish_id', '=', record.polish_id.id),
    #                 ('symmetry_id', '=', record.symmetry_id.id),
    #                 ('florescence_id', '=', record.florescence_id.id),
    #             ]
    #             avg_rap_back_line = self.env['less.discount.line'].search(domain, order='create_date desc', limit=1)
    #             record.avg_rap_back = avg_rap_back_line.avg_rap_back if avg_rap_back_line else 0.00
    #             record.avg_price_per_carat = avg_rap_back_line.avg_per_carat if avg_rap_back_line else 0.00
    #         else:
    #             record.avg_rap_back = 0.00
    #             record.avg_price_per_carat = 0.00

    # @api.depends('avg_price_per_carat', 'rap_price', 'size_id', 'shape_id', 'colour_id', 'clarity_id', 'cut_id', 'polish_id', 'symmetry_id', 'florescence_id')
    # def _compute_price_carat(self):
    #     for data in self:
    #         dir_disc = ind_disc = 0
    #         if data.avg_price_per_carat != 0 and data.rap_price != 0:
    #             if all([data.size_id, data.shape_id, data.colour_id, data.clarity_id, data.cut_id, data.polish_id, data.symmetry_id, data.florescence_id]):
    #                 size_sequence = data.size_id.y_sequence_no
    #                 shape_sequence = data.shape_id.y_sequence_no
    #                 colour_sequence = data.colour_id.y_sequence_no
    #                 clarity_sequence = data.clarity_id.y_sequence_no
    #                 cut_sequence = data.cut_id.y_sequence_no
    #                 polish_sequence = data.polish_id.y_sequence_no
    #                 symmetry_sequence = data.symmetry_id.y_sequence_no
    #                 flor_sequence = data.florescence_id.y_sequence_no
    #                 indirect_domain = [
    #                     ('from_size_id.y_sequence_no', '<=', size_sequence),
    #                     ('to_size_id.y_sequence_no', '>=', size_sequence),
    #                     ('from_shape_id.y_sequence_no', '<=', shape_sequence),
    #                     ('to_shape_id.y_sequence_no', '>=', shape_sequence),
    #                     ('from_clr_id.y_sequence_no', '<=', colour_sequence),
    #                     ('to_clr_id.y_sequence_no', '>=', colour_sequence),
    #                     ('from_clarity_id.y_sequence_no', '<=', clarity_sequence),
    #                     ('to_clarity_id.y_sequence_no', '>=', clarity_sequence),
    #                     ('from_cut_id.y_sequence_no', '<=', cut_sequence),
    #                     ('to_cut_id.y_sequence_no', '>=', cut_sequence),
    #                     ('from_pol_id.y_sequence_no', '<=', polish_sequence),
    #                     ('to_pol_id.y_sequence_no', '>=', polish_sequence),
    #                     ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
    #                     ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
    #                     ('discount_indirect_id.state', '=', 'approved'),
    #                 ]
    #                 ind_discount_line = self.env['discount.indirect.line'].search(indirect_domain, order='approved_date desc', limit=1)
    #                 ind_disc = (ind_discount_line.discount / 100) if ind_discount_line else 0.00
    #                 direct_domain = [
    #                     ('size_from_id.y_sequence_no', '<=', size_sequence),
    #                     ('size_to_id.y_sequence_no', '>=', size_sequence),
    #                     ('shape_id', '=', data.shape_id.id),
    #                     ('colour_id', '=', data.colour_id.id),
    #                     ('clarity_id', '=', data.clarity_id.id),
    #                     ('from_cut_id.y_sequence_no', '<=', cut_sequence),
    #                     ('to_cut_id.y_sequence_no', '>=', cut_sequence),
    #                     ('from_pol_id.y_sequence_no', '<=', polish_sequence),
    #                     ('to_pol_id.y_sequence_no', '>=', polish_sequence),
    #                     ('from_sym_id.y_sequence_no', '<=', symmetry_sequence),
    #                     ('to_sym_id.y_sequence_no', '>=', symmetry_sequence),
    #                     ('from_florescence_id.y_sequence_no', '<=', flor_sequence),
    #                     ('to_florescence_id.y_sequence_no', '>=', flor_sequence),
    #                     ('discount_direct_id.state', '=', 'approved'),
    #                 ]
    #                 dir_disc_line = self.env['discount.direct.line'].search(direct_domain, order='approved_date desc', limit=1)
    #                 dir_disc = (dir_disc_line.discount / 100) if dir_disc_line else 0.00
    #                 data.price_per_carat = data.avg_price_per_carat + (data.avg_price_per_carat * dir_disc) + (data.avg_price_per_carat * ind_disc)
    #                 data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
    #             else:
    #                 data.price_per_carat = data.avg_rap_back
    #                 data.final_rap_back = (data.price_per_carat / data.rap_price - 1) * 100
    #         else:
    #             data.price_per_carat = 0.00
    #             data.final_rap_back = 0.00



    @api.depends('rap_price1', 'price_per_carat1')
    def _compute_final_rap_back(self):
        for record in self:
            if record.rap_price1:
                record.final_rap_back1 = ((record.price_per_carat1 / record.rap_price1) - 1) * 100
            else:
                record.final_rap_back1 = 0.00





    @api.model
    def fetch_and_store_inventory_pricing(self):
        """Fetch inventory data from SimGems API and store in Odoo."""

        auth_url = "http://devapi.simgems.com/api/auth/login"
        stock_url = "http://devapi.simgems.com/api/stock/getfullstock"

        credentials = {
            "username": "developer@simgems.com",
            "password": "Dev@Sim1"
        }

        headers = {"Content-Type": "application/json"}

        import re

        def extract_second_url(link):
            if not isinstance(link, str):  # Ensure input is a valid string
                return None

            # Split the concatenated URLs correctly
            urls = re.split(r'(https?://)', link)  # Splitting while keeping 'http://' part

            # Reconstruct proper URLs
            urls = [urls[i] + urls[i + 1] for i in range(1, len(urls) - 1, 2)]

            return urls[1] if len(urls) > 1 else None  # Return second URL if exists

        try:
            # Authenticate and get token
            auth_response = requests.post(auth_url, json=credentials, headers=headers)
            auth_response.raise_for_status()
            auth_data = auth_response.json()

            if not auth_data.get("success"):
                raise Exception("Authentication Failed")

            token = auth_data["data"]["token"]
            headers["Authorization"] = f"Bearer {token}"

            # Fetch stock data
            stock_response = requests.get(stock_url, headers=headers)
            stock_response.raise_for_status()
            stock_data = stock_response.json()

            if not stock_data.get("success") or "data" not in stock_data:
                raise Exception("Failed to fetch stock data")

            stock_list = stock_data["data"]

            def get_attribute_id(attribute_name):
                if not attribute_name:
                    return False
                attr = self.env['product.attribute.value'].sudo().search(
                    [('name', '=', attribute_name)], limit=1)
                return attr.id if attr else False

            def safe_float(value):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return 0.0

            for item in stock_list:
                vals = {
                     'polish_code': item.get('stockRef'),
                     'certificate_no': item.get('certiNo'),
                     'cert_link': item.get('pdf'),
                     'size': item.get('carat'),
                     'shape_id': get_attribute_id(item.get('shape')),
                     'shape_name': item.get('shape'),
                     'colour': item.get('color'),
                     'colour_id': get_attribute_id(item.get('color')),
                     'clarity_id': get_attribute_id(item.get('clarity')),
                     'cut_id': get_attribute_id(item.get('cut')),
                     'polish_id': get_attribute_id(item.get('polish')),
                     'symmetry_id': get_attribute_id(item.get('symmetry')),
                     'florescence_id': get_attribute_id(item.get('fluorescence')),
                     'image_id': extract_second_url(item.get('diamondImage', '')),
                     'video_id': extract_second_url(item.get('video', '')),
                     'lab_id': get_attribute_id(item.get('lab')),
                     'cert_comments': item.get('certComment'),
                     'key_to_symbols': item.get('kts'),
                     'measurement': item.get('measurements'),
                     'bt_id': get_attribute_id(item.get('bit')),
                     'bc_id': get_attribute_id(item.get('bic')),
                     'wt_id': get_attribute_id(item.get('wit')),
                     'wc_id': get_attribute_id(item.get('wic')),
                     'table_perc': safe_float(item.get('tp')),
                     'depth_perc': safe_float(item.get('td')),
                     'crown_angle': safe_float(item.get('ca')),
                     'pavilion_angle': safe_float(item.get('pa')),
                     'pavilion_depth': safe_float(item.get('ph')),
                     'ec_id': get_attribute_id(item.get('eyeClean')),
                     'country': item.get('location'),
                     'stone_status':item.get('status'),
                     'rap_price1':item.get('rapList'),
                     'price_per_carat1':item.get('ppc'),
                }

                if vals['rap_price1']:
                    vals['final_rap_back1'] = ((vals['price_per_carat1'] / vals['rap_price1']) - 1) * 100
                else:
                    vals['final_rap_back1'] = 0.00

                existing_record = self.env['inventory.pricing'].sudo().search(
                    [('certificate_no', '=', item.get('certiNo'))], limit=1)

                if existing_record:
                    existing_record.write(vals)
                else:
                    self.create(vals)

        except requests.exceptions.RequestException as e:
            self.env.cr.rollback()
            raise Exception(f"Error fetching data: {str(e)}")

