# -*- coding: utf-8 -*-
{
    'name': "inventory_pricing",

    'summary': "To Manage the PLM inventory and Pricinge engines",

    'description': """
To Manage the PLM inventory and Pricinge engines
    """,

    'author': "Simgems",
    'website': "https://www.prixgen.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'PLM',
    'version': '18.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],
    'images': ['static/description/icon.png'],

    # always loaded
    'data': [
        'data/ir_sequence.xml',
        'data/fatch_inventory.xml',
        'security/ir.model.access.csv',
        'views/inventory_pricing_menu_views.xml',
        'views/inventory_pricing_views.xml',
        'views/product_attribute_view.xml',

    ],
    'installable': True,
    'application': True,
}

