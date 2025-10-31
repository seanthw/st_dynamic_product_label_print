{
    "name": "Dynamic Product Label Print",
    'version': '2.2.0',
    "category": "Inventory",
    "summary": "Print product labels with quantities based on stock",
    "description": """
        Print dynamic product labels with variable quantities based on available stock.
        Each product gets different number of labels matching its on-hand quantity.
    """,
    "author": "Sean Thawe",
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/paper_formats.xml',
        'views/product_label_views.xml',
        'views/res_config_settings_views.xml',
        'views/reports.xml',
        'views/product_template_views.xml',
        'data/default_settings.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
}
