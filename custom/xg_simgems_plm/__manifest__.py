# -*- coding: utf-8 -*-
{
    'name': "xg_simgems_plm",

    'summary': "To Manage the PLM datas and Pricinge engines",

    'description': """
To Manage the PLM datas and Pricinge engines
    """,
    

    'author': "Prixgen",
    'website': "https://www.prixgen.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'PLM',
    'version': '18.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','mail','product','mrp_plm'],
    'images': ['static/description/icon.png'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/pricing_engine_data.xml',
        'wizard/pricing_planning_views.xml',
        'views/product_attribute_view.xml',
        'views/discount_indirect_views.xml',
        'views/plm_weightage_views.xml',
        'views/plm_competitor_views.xml',
        'views/discount_direct_views.xml',
        'views/internal_discount_views.xml',
        'views/plm_certification_views.xml',
        'views/base_price_views.xml',
        'views/discount_capping_views.xml',
        'views/competitor_discount_views.xml',
        'views/rapprice_threshold_views.xml',
        'views/rap_price_views.xml',
        'views/less_discount_views.xml',
        'views/pricing_engine_views.xml',
        'views/discount_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
        'xg_simgems_plm/static/src/radio_image_field/custom_radio_image.js',
        'xg_simgems_plm/static/src/radio_image_field/custom_radio_image.xml', 
        'xg_simgems_plm/static/src/scss/image.scss',
    ],
    
    },
    'installable': True,
    'application': True,
}

