# -*- coding: utf-8 -*-

def _setup_default_paperformat(env):
    """Set the default paper format for the module."""
    paperformat_id = env.ref("st_dynamic_product_label_print.paperformat_label_sheet", raise_if_not_found=False)
    if paperformat_id:
        env["ir.config_parameter"].sudo().set_param(
            "st_dynamic_product_label_print.paperformat_id",
            paperformat_id.id
        )
