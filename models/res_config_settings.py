# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    label_rows = fields.Integer(string='Number of Rows')
    label_cols = fields.Integer(string='Number of Columns')
    label_paperformat_id = fields.Many2one('report.paperformat', string='Paper Format')
    label_show_barcode_digits = fields.Boolean(string='Show Barcode Digits')
    label_show_internal_ref = fields.Boolean(string='Show Internal Reference')
    label_show_on_hand_qty = fields.Boolean(string='Show On-Hand Quantity')
    label_show_attributes = fields.Boolean(string='Show Attributes')
    label_font_size = fields.Integer(string='Base Font Size (px)')
    label_margin_top = fields.Integer(string='Top Margin (mm)')
    label_margin_bottom = fields.Integer(string='Bottom Margin (mm)')
    label_margin_left = fields.Integer(string='Left Margin (mm)')
    label_margin_right = fields.Integer(string='Right Margin (mm)')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param('st_dynamic_product_label_print.label_rows', self.label_rows)
        ICP.set_param('st_dynamic_product_label_print.label_cols', self.label_cols)
        ICP.set_param('st_dynamic_product_label_print.label_paperformat_id', self.label_paperformat_id.id or 0)
        ICP.set_param('st_dynamic_product_label_print.label_show_barcode_digits', self.label_show_barcode_digits)
        ICP.set_param('st_dynamic_product_label_print.label_show_internal_ref', self.label_show_internal_ref)
        ICP.set_param('st_dynamic_product_label_print.label_show_on_hand_qty', self.label_show_on_hand_qty)
        ICP.set_param('st_dynamic_product_label_print.label_show_attributes', self.label_show_attributes)
        ICP.set_param('st_dynamic_product_label_print.label_font_size', self.label_font_size)
        ICP.set_param('st_dynamic_product_label_print.label_margin_top', self.label_margin_top)
        ICP.set_param('st_dynamic_product_label_print.label_margin_bottom', self.label_margin_bottom)
        ICP.set_param('st_dynamic_product_label_print.label_margin_left', self.label_margin_left)
        ICP.set_param('st_dynamic_product_label_print.label_margin_right', self.label_margin_right)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        res.update(
            label_rows=int(ICP.get_param('st_dynamic_product_label_print.label_rows', 7)),
            label_cols=int(ICP.get_param('st_dynamic_product_label_print.label_cols', 2)),
            label_paperformat_id=int(ICP.get_param('st_dynamic_product_label_print.label_paperformat_id', 0)) or False,
            label_show_barcode_digits=ICP.get_param('st_dynamic_product_label_print.label_show_barcode_digits') == 'True',
            label_show_internal_ref=ICP.get_param('st_dynamic_product_label_print.label_show_internal_ref') == 'True',
            label_show_on_hand_qty=ICP.get_param('st_dynamic_product_label_print.label_show_on_hand_qty') == 'True',
            label_show_attributes=ICP.get_param('st_dynamic_product_label_print.label_show_attributes') == 'True',
            label_font_size=int(ICP.get_param('st_dynamic_product_label_print.label_font_size', 12)),
            label_margin_top=int(ICP.get_param('st_dynamic_product_label_print.label_margin_top', 5)),
            label_margin_bottom=int(ICP.get_param('st_dynamic_product_label_print.label_margin_bottom', 5)),
            label_margin_left=int(ICP.get_param('st_dynamic_product_label_print.label_margin_left', 5)),
            label_margin_right=int(ICP.get_param('st_dynamic_product_label_print.label_margin_right', 5)),
        )
        return res