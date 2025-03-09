# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Frontdesk Custom",
    "version": "18.0.0.0",
    "license": "AGPL-3",
    "summary": "Simgems Scope and Customizations",
    "author": "Simgems",
    "maintainer": "Simgems",
    "website": "https://www.simgems.com",
    "application": True,
    "sequence": 0,
    "depends": ['base','frontdesk',
    ],

    'images': ['static/description/icon.png'],

    "data": [
    'security/ir.model.access.csv',
    'views/visitor_form_views.xml',
    # 'views/visitor_form.xml',
    ],
    'assets': {
        'frontdesk.assets_frontdesk': [
            'frontdesk_custom/static/src/visitor_form/visitor_form.js',
            'frontdesk_custom/static/src/visitor_form/visitor_form.xml',
            'frontdesk_custom/static/src/visitor_form/navbar_form.xml',
            'frontdesk_custom/static/src/visitor_form/welcome_page.xml',
            'frontdesk_custom/static/src/visitor_form/custom_style.scss',
            'frontdesk_custom/static/src/visitor_form/welcome_form.js',
        ],
    },
}
