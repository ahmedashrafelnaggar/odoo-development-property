# -*- coding: utf-8 -*-
{
    'name': "om_odoo_inheritence",

    'summary': "",

    'description': """
    """,

    'author': "Ahmed Ashraf Elnaggar",
    'website': "",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management','contact','mail',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}

