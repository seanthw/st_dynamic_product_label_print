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
    rows = fields.Integer(
        string="Rows",
        required=True,
        default=lambda self: self.env['res.config.settings'].default_get(['label_rows']).get('label_rows', 10),
    )
    cols = fields.Integer(
        string="Columns",
        required=True,
        default=lambda self: self.env['res.config.settings'].default_get(['label_cols']).get('label_cols', 3),
    )
    skipped_pages = fields.Integer(string="Skip Full Pages", default=0)
    start_row = fields.Integer(string="Start Row", default=1)
    start_col = fields.Integer(string="Start Column", default=1)

    @api.model
    def default_get(self, fields_list):
        """Load default values from system configuration."""
        res = super().default_get(fields_list)
        get_param = self.env["ir.config_parameter"].sudo().get_param
        
        default_paperformat_id = get_param("st_dynamic_product_label_print.paperformat_id")
        if default_paperformat_id:
            res["paperformat_id"] = int(default_paperformat_id)
            
        return res

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

    def _get_config_params(self):
        """Fetch all required configuration parameters at once."""
        get_param = self.env["ir.config_parameter"].sudo().get_param
        return {
            "paperformat_id": int(get_param("st_dynamic_product_label_print.paperformat_id", 0)),
            "margin_top": int(get_param("st_dynamic_product_label_print.label_margin_top", 10)),
            "margin_bottom": int(get_param("st_dynamic_product_label_print.label_margin_bottom", 10)),
            "margin_left": int(get_param("st_dynamic_product_label_print.label_margin_left", 10)),
            "margin_right": int(get_param("st_dynamic_product_label_print.label_margin_right", 10)),
            "font_size": int(get_param("st_dynamic_product_label_print.label_font_size", 16)),
            "label_width": float(get_param("st_dynamic_product_label_print.label_width", 70.0)),
            "label_height": float(get_param("st_dynamic_product_label_print.label_height", 35.0)),
            "show_barcode_digits": get_param("st_dynamic_product_label_print.label_show_barcode_digits") == "True",
            "show_internal_ref": get_param("st_dynamic_product_label_print.label_show_internal_ref") == "True",
            "show_on_hand_qty": get_param("st_dynamic_product_label_print.label_show_on_hand_qty") == "True",
            "show_stock_label": get_param("st_dynamic_product_label_print.label_show_stock_label") == "True",
            "show_attributes": get_param("st_dynamic_product_label_print.label_show_attributes") == "True",
            "reference_width": float(get_param("st_dynamic_product_label_print.label_reference_width", 70.0)),
            "reference_height": float(get_param("st_dynamic_product_label_print.label_reference_height", 35.0)),
        }

    def _validate_inputs(self):
        """Validate user inputs before proceeding."""
        self.ensure_one()
        if not self.product_ids:
            raise UserError(_("You must select at least one product."))
        if self.start_row < 1 or self.start_row > self.rows:
            raise UserError(_("Start Row must be between 1 and %d.") % self.rows)
        if self.start_col < 1 or self.start_col > self.cols:
            raise UserError(_("Start Column must be between 1 and %d.") % self.cols)
        if self.skipped_pages < 0:
            raise UserError(_("Skipped Pages must be a positive number."))

    def _calculate_font_size(self, base_font_size):
        """Calculate a scaled font size based on rows and columns."""
        return base_font_size

    def _calculate_dynamic_styles(self, label_width, label_height, base_font_size, reference_width, reference_height):
        """Calculate dynamic style properties based on label dimensions."""
        
        # 1. Calculate a reasonable font size
        width_ratio = label_width / reference_width if reference_width else 1
        height_ratio = label_height / reference_height if reference_height else 1
        # Use a less aggressive scaling factor for font size
        font_size = base_font_size * (min(width_ratio, height_ratio) * 0.7 + 0.3)
        font_size = max(font_size, 11) # Set a minimum font size of 11px

        # 2. Calculate barcode max height
        barcode_max_height = label_height * 0.25 # Barcode can take up to 25% of the height

        # 3. Calculate vertical padding
        padding_vertical = label_height * 0.05 # 5% top/bottom padding
        
        return {
            'font_size': f"{font_size:.2f}px",
            'padding': f"{padding_vertical:.2f}mm 1mm", # Vertical padding, fixed horizontal
            'barcode_max_height': f"{barcode_max_height:.2f}mm",
        }

    def _prepare_label_data(self, font_size, label_width, label_height, reference_width, reference_height):
        """Prepare the list of dictionaries for each label to be printed."""
        label_data = []
        
        dynamic_styles = self._calculate_dynamic_styles(label_width, label_height, font_size, reference_width, reference_height)

        for product in self.product_ids:
            quantity = (
                product.qty_available
                if self.label_quantity == "on_hand"
                else self.custom_quantity
            )
            quantity = max(int(quantity), 0)
            attribute_string = " ".join(
                product.product_template_attribute_value_ids.mapped("name")
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
        self._validate_inputs()
        config = self._get_config_params()
        
        paperformat = self.paperformat_id
        if not paperformat:
            if config.get("paperformat_id"):
                paperformat = self.env["report.paperformat"].browse(config["paperformat_id"])
            else:
                raise UserError(_("You must either select a paper format in the wizard or set a default paper format in the settings."))

        # Calculate available height and adjust label height if necessary
        # Extra height per label for padding (in mm)
        # 1mm padding top and bottom for the table cell = 2mm
        extra_height_per_label = 2
        available_height = paperformat.page_height - config["margin_top"] - config["margin_bottom"]
        required_height = self.rows * (config["label_height"] + extra_height_per_label)
        
        if required_height > available_height:
            label_height = (available_height / self.rows) - extra_height_per_label
        else:
            label_height = config["label_height"]

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

        # Prepare a single flat list of all labels
        all_labels = self._prepare_label_data(
            config["font_size"], 
            config["label_width"], 
            label_height, 
            config["reference_width"], 
            config["reference_height"]
        )
        
        # Add offsets for skipped cells
        offset = (self.start_row - 1) * self.cols + (self.start_col - 1)
        all_labels = ([{}] * offset) + all_labels

        # Calculate page numbers
        if self.rows <= 0 or self.cols <= 0:
            raise UserError(_("The number of rows and columns must be greater than zero."))
        labels_per_page = self.rows * self.cols
        if not labels_per_page:
            raise UserError(_("Please configure the number of rows and columns for the labels."))
        page_numbers = math.ceil(len(all_labels) / labels_per_page)

        data = {
            "labels": all_labels,
            "page_numbers": int(page_numbers),
            "labels_per_page": labels_per_page,
            "rows": self.rows,
            "cols": self.cols,
            "label_width": config["label_width"],
            "label_height": label_height,
            **config,
        }

        data.update({
            "show_barcode_digits": self.show_barcode_digits,
            "show_internal_ref": self.show_internal_ref,
            "show_on_hand_qty": self.show_on_hand_qty,
            "show_stock_label": self.show_stock_label,
            "show_attributes": self.show_attributes,
        })

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

    def action_print_labels(self):
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
