# -*- coding: utf-8 -*-

def _setup_default_paperformat(env):
    # Set default paperformat
    paperformat_id = env.ref('stock.paperformat_label_sheet_a4', raise_if_not_found=False)
    if paperformat_id:
        env['ir.config_parameter'].sudo().set_param(
            'st_dynamic_product_label_print.paperformat_id', 
            paperformat_id.id
        )
