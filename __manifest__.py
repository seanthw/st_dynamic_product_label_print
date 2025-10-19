{
    "name": "Dynamic Product Label Print",
    'version': '1.1.6',
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
        "views/paper_formats.xml",
        "views/product_template_views.xml",
        "views/product_label_views.xml",
        "views/reports.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
