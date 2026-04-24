{
    'name': 'Estate Sample',
    'version': '1.0',
    'depends': ['base', 'website_sale'], # ضفنا website_sale هنا
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/website_templates.xml', # هنكريت الملف ده دلوقتي
    ],
    'installable': True,
    'application': True,
}