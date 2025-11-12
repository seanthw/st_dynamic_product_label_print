import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductLabelWizard(models.TransientModel):
    _name = "product.label.wizard"
    _description = "Product Label Printing Wizard"

    product_ids = fields.Many2many("product.product", string="Products", required=True)
    label_quantity = fields.Selection(
        [
            ("on_hand", "Based On Hand Quantity"),
            ("custom", "Custom Quantity"),
        ],
        string="Quantity Type",
        default="on_hand",
        required=True,
    )
    custom_quantity = fields.Integer(string="Custom Quantity", default=1)
    paperformat_id = fields.Many2one(
        "report.paperformat",
        string="Paper Format",
        required=False,
    )
    print_format = fields.Selection(
        [
            ("2x10", "2 x 10"),
            ("3x10", "3 x 10"),
            ("other", "Other"),
        ],
        string="Label Format",
        default="3x10",
        required=True,
    )
    rows = fields.Integer(
        string="Rows",
        required=True,
        default=10,
    )
    cols = fields.Integer(
        string="Columns",
        required=True,
        default=3,
    )
    vertical_spacing = fields.Float(
        string="Vertical Spacing (mm)",
        required=True,
        default=0.0,
    )
    horizontal_spacing = fields.Float(
        string="Horizontal Spacing (mm)",
        required=True,
        default=3.0,
    )

    @api.onchange('print_format')
    def _onchange_print_format(self):
        if self.print_format == '2x10':
            self.rows = 10
            self.cols = 2
        elif self.print_format == '3x10':
            self.rows = 10
            self.cols = 3

    @api.model
    def default_get(self, fields_list):
        """Load default values from system configuration."""
        res = super().default_get(fields_list)
        get_param = self.env["ir.config_parameter"].sudo().get_param
        
        default_paperformat_id = get_param("st_dynamic_product_label_print.paperformat_id")
        if default_paperformat_id:
            res["paperformat_id"] = int(default_paperformat_id)
            
        res['print_format'] = get_param('st_dynamic_product_label_print.print_format', '3x10')
        res['rows'] = int(get_param('st_dynamic_product_label_print.rows', 10))
        res['cols'] = int(get_param('st_dynamic_product_label_print.cols', 3))
        res['vertical_spacing'] = float(get_param('st_dynamic_product_label_print.label_vertical_spacing', 1.0))
        res['horizontal_spacing'] = float(get_param('st_dynamic_product_label_print.label_horizontal_spacing', 1.0))

        return res

    show_barcode = fields.Boolean(
        string="Show Barcode Image",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param("st_dynamic_product_label_print.label_show_barcode") == "True"
    )
    show_barcode_digits = fields.Boolean(
        string="Show Barcode Digits",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param("st_dynamic_product_label_print.label_show_barcode_digits") == "True"
    )
    show_internal_ref = fields.Boolean(
        string="Show Internal Reference",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param("st_dynamic_product_label_print.label_show_internal_ref") == "True"
    )
    show_on_hand_qty = fields.Boolean(
        string="Show On-Hand Quantity",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param("st_dynamic_product_label_print.label_show_on_hand_qty") == "True"
    )
    show_stock_label = fields.Boolean(
        string="Show Stock Label",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param("st_dynamic_product_label_print.label_show_stock_label") == "True"
    )
    show_attributes = fields.Boolean(
        string="Show Attributes",
        default=lambda self: self.env["ir.config_parameter"].sudo().get_param("st_dynamic_product_label_print.label_show_attributes") == "True"
    )

    def _save_defaults(self):
        """Save the current wizard settings as the new default values."""
        self.ensure_one()
        ICP = self.env['ir.config_parameter'].sudo()
        
        # Mapping of wizard fields to their corresponding system parameter keys
        param_mapping = {
            'print_format': 'st_dynamic_product_label_print.print_format',
            'rows': 'st_dynamic_product_label_print.rows',
            'cols': 'st_dynamic_product_label_print.cols',
            'vertical_spacing': 'st_dynamic_product_label_print.label_vertical_spacing',
            'horizontal_spacing': 'st_dynamic_product_label_print.label_horizontal_spacing',
            'show_barcode': 'st_dynamic_product_label_print.label_show_barcode',
            'show_barcode_digits': 'st_dynamic_product_label_print.label_show_barcode_digits',
            'show_internal_ref': 'st_dynamic_product_label_print.label_show_internal_ref',
            'show_on_hand_qty': 'st_dynamic_product_label_print.label_show_on_hand_qty',
            'show_stock_label': 'st_dynamic_product_label_print.label_show_stock_label',
            'show_attributes': 'st_dynamic_product_label_print.label_show_attributes',
            'paperformat_id': 'st_dynamic_product_label_print.paperformat_id',
        }
        
        for field_name, param_key in param_mapping.items():
            value = self[field_name]
            # For many2one fields, we store the ID
            if isinstance(value, models.BaseModel):
                value = value.id
            
            ICP.set_param(param_key, value)

    def _get_config_params(self):
        """Fetch all required configuration parameters at once."""
        get_param = self.env["ir.config_parameter"].sudo().get_param
        return {
            "paperformat_id": int(get_param("st_dynamic_product_label_print.paperformat_id", 0)),
            "margin_top": float(get_param("st_dynamic_product_label_print.label_margin_top", 12.7)),
            "margin_bottom": float(get_param("st_dynamic_product_label_print.label_margin_bottom", 12.7)),
            "margin_left": float(get_param("st_dynamic_product_label_print.label_margin_left", 5.0)),
            "margin_right": float(get_param("st_dynamic_product_label_print.label_margin_right", 5.0)),
            "font_size": float(get_param("st_dynamic_product_label_print.label_font_size", 10.0)),
            "label_width": float(get_param("st_dynamic_product_label_print.label_width", 66.675)),
            "label_height": float(get_param("st_dynamic_product_label_print.label_height", 25.4)),
            "vertical_spacing": float(get_param("st_dynamic_product_label_print.label_vertical_spacing", 4.0)),
            "horizontal_spacing": float(get_param("st_dynamic_product_label_print.label_horizontal_spacing", 3.0)),
            "show_barcode_digits": get_param("st_dynamic_product_label_print.label_show_barcode_digits") == "True",
            "show_internal_ref": get_param("st_dynamic_product_label_print.label_show_internal_ref") == "True",
            "show_on_hand_qty": get_param("st_dynamic_product_label_print.label_show_on_hand_qty") == "True",
            "show_stock_label": get_param("st_dynamic_product_label_print.label_show_stock_label") == "True",
            "show_attributes": get_param("st_dynamic_product_label_print.label_show_attributes") == "True",
        }

    def _validate_inputs(self):
        """Validate user inputs before proceeding."""
        self.ensure_one()
        if not self.product_ids:
            raise UserError(_("You must select at least one product."))

    def _calculate_dynamic_styles(self, base_font_size, product_name, attribute_string, show_attributes):
        """
        Calculate a simplified, more robust font size.
        The font size is only scaled down if the text is too long, making it predictable.
        """
        font_size = base_font_size
        
        # Determine the total length of the text that will be displayed.
        total_len = len(product_name)
        if show_attributes and attribute_string:
            total_len += len(attribute_string)

        # Define a simple character limit threshold.
        # This can be adjusted, but 45 is a reasonable baseline for a typical label.
        char_limit = 999

        # If the text is longer than the limit, scale the font size down.
        if total_len > char_limit:
            scale_factor = char_limit / total_len
            font_size *= scale_factor

        # Clamp the font size to a reasonable minimum to ensure readability.
        final_font_size = font_size

        return {
            'font_size': final_font_size,
        }

    def _prepare_label_data(self, font_size, label_width, label_height, cols):
        """Prepare the list of dictionaries for each label to be printed."""
        label_data = []

        for product in self.product_ids:
            quantity = (
                product.qty_available
                if self.label_quantity == "on_hand"
                else self.custom_quantity
            )
            quantity = max(int(quantity), 0)
            attribute_string = ", ".join(
                f"{attr_value.attribute_line_id.attribute_id.name}: {attr_value.name}"
                for attr_value in product.product_template_attribute_value_ids
            )

            dynamic_styles = self._calculate_dynamic_styles(
                font_size, product.name, attribute_string, self.show_attributes
            )

            for i in range(quantity):
                label_info = {
                    "product_name": product.name,
                    "attribute_string": attribute_string,
                    "default_code": product.default_code or "",
                    "barcode": product.barcode or "",
                    "sequence": i + 1,
                    "total_quantity": quantity,
                    "on_hand_qty": product.qty_available,
                }
                label_info.update(dynamic_styles)
                label_data.append(label_info)
        return label_data

    def action_print_labels(self):
        self._save_defaults()
        self._validate_inputs()
        config = self._get_config_params()
        
        paperformat = self.paperformat_id or self.env.ref("st_dynamic_product_label_print.paperformat_label", raise_if_not_found=False)
        if not paperformat:
            raise UserError(_("Paper format is not configured. Please set a default in settings or select one in the wizard."))

        # Create a temporary paper format with the dynamic margins.
        temp_paperformat = paperformat.copy({
            "name": f"Dynamic Label Paperformat - {self.id}",
            "margin_top": config["margin_top"],
            "margin_bottom": config["margin_bottom"],
            "margin_left": config["margin_left"],
            "margin_right": config["margin_right"],
        })

        report = self.env.ref("st_dynamic_product_label_print.action_report_product_labels")
        report.paperformat_id = temp_paperformat.id

        # Prepare a single flat list of all labels. The template will handle all layout logic.
        all_labels = self._prepare_label_data(
            config["font_size"],
            0, # Width is now 100% handled by the template
            0, # Height is now 100% handled by the template
            self.cols
        )

        data = {
            "labels": all_labels,
            "rows": self.rows,
            "cols": self.cols,
            "vertical_spacing": self.vertical_spacing,
            "horizontal_spacing": self.horizontal_spacing,
            **config,
            "show_barcode": self.show_barcode,
            "show_barcode_digits": self.show_barcode_digits,
            "show_internal_ref": self.show_internal_ref,
            "show_on_hand_qty": self.show_on_hand_qty,
            "show_stock_label": self.show_stock_label,
            "show_attributes": self.show_attributes,
        }

        report_action = report.report_action(None, data=data)
        report_action.update({"close_on_report_download": True})
        return report_action


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_print_product_labels(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Print Product Labels",
            "res_model": "product.label.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_ids": [(6, 0, self.product_variant_ids.ids)],
            },
        }


class ProductProduct(models.Model):
    _inherit = "product.product"
    def action_print_product_labels(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Print Product Labels",
            "res_model": "product.label.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_ids": [(6, 0, self.ids)],
            },
        }
