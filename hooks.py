# -*- coding: utf-8 -*-

def _set_internal_ref_default(env):
    """
    Set the default value for showing the internal reference on labels.
    This hook ensures that on module installation or update, the default
    is set to False, overriding any previously stored value.
    """
    ICP = env['ir.config_parameter'].sudo()
    ICP.set_param('st_dynamic_product_label_print.label_show_internal_ref', False)

def post_init_hook(cr, registry):
    """
    The post-init hook.
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    _set_internal_ref_default(env)