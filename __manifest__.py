{
    "name": "Dynamic Product Label Print",
    'version': '2.1.0',
    "category": "Inventory",
    "summary": "Print product labels with quantities based on stock",
    "description": """
        Print dynamic product labels with variable quantities based on available stock.
        Each product gets different number of labels matching its on-hand quantity.
    """,
    "author": "Sean Thawe",
    "depends": ["stock", "product", "base_setup"],
    "data": [
        "security/ir.model.access.csv",
        "data/default_settings.xml",
        "views/paper_formats.xml",
        "views/product_template_views.xml",
        "views/product_label_views.xml",
        "views/reports.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "post_init_hook": "_setup_default_paperformat",
}
