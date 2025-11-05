# -*- coding: utf-8 -*-

def _create_default_parameters(env):
    """
    Create default system parameters for the module if they don't exist.
    This is the robust way to set initial values, avoiding errors on upgrade.
    """
    ICP = env['ir.config_parameter'].sudo()
    
    default_params = {
        'st_dynamic_product_label_print.rows': '10',
        'st_dynamic_product_label_print.cols': '3',
        'st_dynamic_product_label_print.label_width': '66.675',
        'st_dynamic_product_label_print.label_height': '25.4',
        'st_dynamic_product_label_print.label_vertical_spacing': '0.0',
        'st_dynamic_product_label_print.label_horizontal_spacing': '3.0',
        'st_dynamic_product_label_print.label_show_barcode': 'True',
        'st_dynamic_product_label_print.label_show_barcode_digits': 'True',
        'st_dynamic_product_label_print.label_show_internal_ref': 'False',
        'st_dynamic_product_label_print.label_show_on_hand_qty': 'True',
        'st_dynamic_product_label_print.label_show_attributes': 'True',
        'st_dynamic_product_label_print.label_font_size': '14',
        'st_dynamic_product_label_print.label_margin_top': '12.7',
        'st_dynamic_product_label_print.label_margin_bottom': '12.7',
        'st_dynamic_product_label_print.label_margin_left': '5',
        'st_dynamic_product_label_print.label_margin_right': '5',
    }
    
    for key, value in default_params.items():
        if not ICP.get_param(key):
            ICP.set_param(key, value)

def post_init_hook(env):
    """
    The post-init hook.
    """
    _create_default_parameters(env)
