from odoo import http
from odoo.http import request
import json

class InventoryPricingAPI(http.Controller):

    @http.route('/api/inventory_pricing', type='json', auth='user', methods=['POST'], csrf=False)
    def create_inventory_pricing(self):
        """API to receive inventory pricing data and create records in Odoo"""
        try:
            data = request.httprequest.get_json()
            if not data:
                return {'status': 'error', 'message': 'No data received'}

            def get_attribute_id(attribute_name):
                """Find the ID of product.attribute.value by name"""
                attr = request.env['product.attribute.value'].sudo().search([('name', '=', attribute_name)], limit=1)
                return attr.id if attr else False

            # Convert names to IDs
            vals = {
                'polish_code': data.get('polish_code'),
                'certificate_no': data.get('certificate_no'),
                'size_id': get_attribute_id(data.get('size')),
                'shape_id': get_attribute_id(data.get('shape')),
                'colour_id': get_attribute_id(data.get('colour')),
                'clarity_id': get_attribute_id(data.get('clarity')),
                'cut_id': get_attribute_id(data.get('cut')) or False,  # Fix for missing value
                'polish_id': get_attribute_id(data.get('polish')) or False,
                'symmetry_id': get_attribute_id(data.get('symmetry')) or False,
                'florescence_id': get_attribute_id(data.get('florescence')),
                'bt_id': get_attribute_id(data.get('black_table_inclusion')),
                'bc_id': get_attribute_id(data.get('black_crown_inclusion')),
                'wt_id': get_attribute_id(data.get('white_table_inclusion')),
                'wc_id': get_attribute_id(data.get('white_crown_inclusion')),
                'shade_id': get_attribute_id(data.get('shade')),
                'heart_id': get_attribute_id(data.get('heart_arrow')) or False,
                'ec_id': get_attribute_id(data.get('eye_clean')) or False,
                'luster_id': get_attribute_id(data.get('luster')) or False,
                'lab_id': get_attribute_id(data.get('lab')),
                'diamond_type_id': get_attribute_id(data.get('diamond_type')) or False,
                'image_id': data.get('image_id'),
                'video_id': data.get('video_id'),
                'cert_comments': data.get('cert_comments'),
                'key_to_symbols': data.get('key_to_symbols'),
                'status': data.get('status'),
                'measurement': data.get('measurement'),
                'table_perc': data.get('table_perc'),
                'depth_perc': data.get('depth_perc'),
                'crown_angle': data.get('crown_angle'),
                'pavilion_angle': data.get('pavilion_angle'),
                'pavilion_depth': data.get('pavilion_depth'),
            }

            # Create record in Odoo
            record = request.env['inventory.pricing'].sudo().create(vals)

            return {'status': 'success', 'message': 'Record created', 'record_id': record.id}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}