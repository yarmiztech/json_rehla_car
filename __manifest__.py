# -*- coding: utf-8 -*-
{
    'name': "JSON For Rehla Car",
    'author':
        'Enzapps',
    'summary': """
This module consist of json objects for Sales,Purchase
""",

    'description': """
        This module consist of track page of cargo which extend the website.
        It consist of 2 tabs Brief and History
    """,
    'website': "",
    'category': 'base',
    'version': '12.0',
    'depends': ['sale','purchase','base'],
    "images": ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
