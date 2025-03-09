# -*- coding: utf-8 -*-
{
    'name': "Video_dashboard",

    'summary': "Manage and organize all videos efficiently.",

    'description': """
Manage and organize all videos efficiently.
    """,

    'author': "Simstar",
    'website': "https://simgems.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Simstar',
    'version': '18.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],
    'images': ['static/description/icon.png'],

    # always loaded
    'data': [
          'security/ir.model.access.csv',
          'data/ir_sequence.xml',
          'views/video_dashboard_menu_views.xml',
          'views/video_dashboard_views.xml'
    ],
    'installable': True,
    'application': True,
}

