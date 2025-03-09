# -*- coding: utf-8 -*-
from odoo import http
from odoo import http, fields
from odoo.http import request
from odoo.tools import consteq
from odoo.addons.frontdesk.controllers.main import Frontdesk

class KAMController(http.Controller):
    @http.route('/frontdesk/kam_list', type='json', auth='public', methods=['POST'], csrf=False)
    def get_kam_list(self):
        """Returns a list of Key Account Managers with ID and Name"""
        kam_records = request.env['frontdesk.kma'].sudo().search([])  # Fetch all KAMs
        kam_list = [{"id": kam.id, "name": kam.name} for kam in kam_records]  # Convert to ID-Name Dict
        return {"kam_list": kam_list}  # Return as JSON

    @http.route('/frontdesk/visitor/save', type='json', auth='public')
    def save_visitor(self, **kwargs):
        """API to save visitor data"""

        # Extract first element from args (list of dict)
        post_data = request.httprequest.get_json()

        # Debugging: Print received data
        # _logger.info("Received Visitor Data: %s", post_data)
        if 'params' in post_data and 'args' in post_data['params'] and len(post_data['params']['args']) > 0:
            visitor_data = post_data['params']['args'][0]  # Extract first dictionary from the list
        else:
            return {'status': 'error', 'message': 'Invalid request format'}

        # Ensure we get correct values
        visitor_data = {
            'name': visitor_data.get('name', ''),
            'phone': visitor_data.get('phone', ''),
            'email': visitor_data.get('email', ''),
            'company': visitor_data.get('company', ''),
            'check_in': fields.Datetime.now(),
            'kam_id': int(visitor_data.get('kam_id')) if visitor_data.get('kam_id') else False,
            'station_id': int(visitor_data.get('station_id')) if visitor_data.get('station_id') else False,
            'state': 'checked_in'# Convert to int
        }

        visitor = request.env['frontdesk.visitor'].sudo().create(visitor_data)
        visitor._notify()
        return {'status': 'success', 'visitor_id': visitor.id}

class Frontdesk(Frontdesk):
    def _verify_token(self, frontdesk, token):
        if consteq(frontdesk.access_token, token):
            return True
        else:
            time_difference = fields.Datetime.now() - fields.Datetime.from_string(token[-19:])
            if time_difference.total_seconds() <= 604800 and consteq(frontdesk._get_tmp_code(), token[:64]):
                return True
            return False