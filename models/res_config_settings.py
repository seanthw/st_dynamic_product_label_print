# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    label_print_format = fields.Selection(
        [
            ("2x10", "2 x 10"),
            ("3x10", "3 x 10"),
            ("other", "Other"),
        ],
        string="Default Label Format",
        config_parameter="st_dynamic_product_label_print.print_format",
        default="3x10",
    )
    label_rows = fields.Integer(
        string='Default Number of Rows',
        config_parameter="st_dynamic_product_label_print.rows",
        default=10
    )
    label_cols = fields.Integer(
        string='Default Number of Columns',
        config_parameter="st_dynamic_product_label_print.cols",
        default=3
    )
    label_show_barcode = fields.Boolean(
        string='Show Barcode Image',
        config_parameter="st_dynamic_product_label_print.label_show_barcode",
        default=True,
    )
    label_show_barcode_digits = fields.Boolean(
        string='Show Barcode Digits',
        config_parameter="st_dynamic_product_label_print.label_show_barcode_digits",
        default=True,
    )
    label_show_internal_ref = fields.Boolean(
        string='Show Internal Reference',
        config_parameter="st_dynamic_product_label_print.label_show_internal_ref",
        default=False,
    )
    label_show_on_hand_qty = fields.Boolean(string='Show On-Hand Quantity')
    label_show_stock_label = fields.Boolean(string='Show Stock Label')
    label_show_attributes = fields.Boolean(
        "Show Attributes",
        config_parameter="st_dynamic_product_label_print.label_show_attributes",
    )
    label_font_size = fields.Integer(string='Base Font Size (px)')
    label_margin_top = fields.Integer(string='Top Margin (mm)')
    label_margin_bottom = fields.Integer(string='Bottom Margin (mm)')
    label_margin_left = fields.Integer(string='Left Margin (mm)')
    label_margin_right = fields.Integer(string='Right Margin (mm)')
    paperformat_id = fields.Many2one('report.paperformat', string='Default Paper Format')
    label_width = fields.Float(string='Label Width (mm)')
    label_height = fields.Float(string='Label Height (mm)')
    label_vertical_spacing = fields.Float(
        string='Vertical Spacing (mm)',
        config_parameter='st_dynamic_product_label_print.label_vertical_spacing',
        default=0.0
    )
    label_horizontal_spacing = fields.Float(
        string='Horizontal Spacing (mm)',
        config_parameter='st_dynamic_product_label_print.label_horizontal_spacing',
        default=3.0
    )

    @api.model
    def set_default_parameters(self):
        """
        Set the default values for the module's system parameters.
        This is called from a data file to ensure upgrade-safe initialization.
        """
        ICP = self.env['ir.config_parameter'].sudo()
        
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



    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICP = self.env['ir.config_parameter'].sudo()

        ICP.set_param('st_dynamic_product_label_print.label_show_on_hand_qty', self.label_show_on_hand_qty)
        ICP.set_param('st_dynamic_product_label_print.label_show_stock_label', self.label_show_stock_label)
        ICP.set_param('st_dynamic_product_label_print.label_font_size', self.label_font_size)
        ICP.set_param('st_dynamic_product_label_print.label_margin_top', self.label_margin_top)
        ICP.set_param('st_dynamic_product_label_print.label_margin_bottom', self.label_margin_bottom)
        ICP.set_param('st_dynamic_product_label_print.label_margin_left', self.label_margin_left)
        ICP.set_param('st_dynamic_product_label_print.label_margin_right', self.label_margin_right)
        ICP.set_param('st_dynamic_product_label_print.paperformat_id', self.paperformat_id.id)
        ICP.set_param('st_dynamic_product_label_print.label_width', self.label_width)
        ICP.set_param('st_dynamic_product_label_print.label_height', self.label_height)


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        
        paperformat_id_param = ICP.get_param('st_dynamic_product_label_print.paperformat_id')
        paperformat_id = int(paperformat_id_param) if paperformat_id_param and paperformat_id_param.isdigit() else False

        res.update(

            label_show_on_hand_qty=ICP.get_param('st_dynamic_product_label_print.label_show_on_hand_qty') == 'True',
            label_show_stock_label=ICP.get_param('st_dynamic_product_label_print.label_show_stock_label') == 'True',
            label_font_size=int(ICP.get_param('st_dynamic_product_label_print.label_font_size')),
            label_margin_top=float(ICP.get_param('st_dynamic_product_label_print.label_margin_top')),
            label_margin_bottom=float(ICP.get_param('st_dynamic_product_label_print.label_margin_bottom')),
            label_margin_left=float(ICP.get_param('st_dynamic_product_label_print.label_margin_left')),
            label_margin_right=float(ICP.get_param('st_dynamic_product_label_print.label_margin_right')),
            paperformat_id=paperformat_id,
            label_width=float(ICP.get_param('st_dynamic_product_label_print.label_width', 68.63)),
            label_height=float(ICP.get_param('st_dynamic_product_label_print.label_height', 25.4)),

        )
        return res
