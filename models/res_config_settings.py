# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    label_rows = fields.Integer(
        string='Number of Rows',
        config_parameter='st_dynamic_product_label_print.label_rows',
        default=7,
        help="Define how many rows of labels are on a single page."
    )
    label_cols = fields.Integer(
        string='Number of Columns',
        config_parameter='st_dynamic_product_label_print.label_cols',
        default=2,
        help="Define how many columns of labels are on a single page."
    )
    label_paperformat_id = fields.Many2one(
        'report.paperformat',
        string='Paper Format',
        config_parameter='st_dynamic_product_label_print.label_paperformat_id',
        help="Select the paper format to use for printing labels."
    )
    label_show_barcode_digits = fields.Boolean(
        string='Show Barcode Digits',
        config_parameter='st_dynamic_product_label_print.label_show_barcode_digits',
        default=True,
        help="If checked, the barcode's numerical digits will be displayed below the barcode image."
    )
    label_show_internal_ref = fields.Boolean(
        string='Show Internal Reference',
        config_parameter='st_dynamic_product_label_print.label_show_internal_ref',
        default=True
    )
    label_show_on_hand_qty = fields.Boolean(
        string='Show On-Hand Quantity',
        config_parameter='st_dynamic_product_label_print.label_show_on_hand_qty',
        default=True
    )
    label_show_attributes = fields.Boolean(
        string='Show Attributes',
        config_parameter='st_dynamic_product_label_print.label_show_attributes',
        default=True
    )
    label_font_size = fields.Integer(
        string='Base Font Size (px)',
        config_parameter='st_dynamic_product_label_print.label_font_size',
        default=12
    )
    label_margin_top = fields.Integer(
        string='Top Margin (mm)',
        config_parameter='st_dynamic_product_label_print.label_margin_top',
        default=5
    )
    label_margin_bottom = fields.Integer(
        string='Bottom Margin (mm)',
        config_parameter='st_dynamic_product_label_print.label_margin_bottom',
        default=5
    )
    label_margin_left = fields.Integer(
        string='Left Margin (mm)',
        config_parameter='st_dynamic_product_label_print.label_margin_left',
        default=5
    )
    label_margin_right = fields.Integer(
        string='Right Margin (mm)',
        config_parameter='st_dynamic_product_label_print.label_margin_right',
        default=5
    )
