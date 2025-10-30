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
    rows = fields.Integer(string="Rows", required=True)
    cols = fields.Integer(string="Columns", required=True)
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
            
        default_rows = get_param("st_dynamic_product_label_print.label_rows")
        if default_rows:
            res["rows"] = int(default_rows)
            
        default_cols = get_param("st_dynamic_product_label_print.label_cols")
        if default_cols:
            res["cols"] = int(default_cols)
            
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
        if self.start_row < 1 or self.start_row > self.rows:
            raise UserError(_("Start Row must be between 1 and %d.") % self.rows)
        if self.start_col < 1 or self.start_col > self.cols:
            raise UserError(_("Start Column must be between 1 and %d.") % self.cols)
        if self.skipped_pages < 0:
            raise UserError(_("Skipped Pages must be a positive number."))

    def _calculate_font_size(self, base_font_size):
        """Calculate a scaled font size based on rows and columns."""
        return base_font_size

    def _prepare_label_data(self, font_size):
        """Prepare the list of dictionaries for each label to be printed."""
        label_data = []
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
                label_data.append({
                    "product_name": product.name,
                    "attribute_string": attribute_string,
                    "default_code": product.default_code or "",
                    "barcode": product.barcode or "",
                    "sequence": i + 1,
                    "total_quantity": quantity,
                    "on_hand_qty": product.qty_available,
                    "font_size": font_size,
                })
        return label_data

    def _prepare_pages(self, label_data):
        """Arrange label data into pages with offsets and skipped pages."""
        full_per_page = self.rows * self.cols
        offset = (self.start_row - 1) * self.cols + (self.start_col - 1)

        # Create a single list of all items to be placed on the grid
        all_items = ([{}] * offset) + label_data

        # Chunk this list into pages of size full_per_page
        pages = [
            all_items[i : i + full_per_page]
            for i in range(0, len(all_items), full_per_page)
        ]

        # Pad the last page to ensure it's a full grid, which is crucial for the renderer
        if pages and len(pages[-1]) < full_per_page:
            pages[-1].extend([{}] * (full_per_page - len(pages[-1])))

        # Add blank pages if requested
        if self.skipped_pages > 0:
            blank_page = [{}] * full_per_page
            pages = ([blank_page] * self.skipped_pages) + pages
            
        return pages

    def action_print_labels(self):
        self._validate_inputs()
        config = self._get_config_params()
        
        paperformat = self.paperformat_id
        if not paperformat:
            if config.get("paperformat_id"):
                paperformat = self.env["report.paperformat"].browse(config["paperformat_id"])
            else:
                raise UserError(_("You must either select a paper format in the wizard or set a default paper format in the settings."))

        # Create a temporary paper format with the dynamic margins. This is the correct Odoo practice.
        temp_paperformat = paperformat.copy({
            "name": f"Dynamic Label Paperformat - {self.id}",
            "margin_top": config["margin_top"],
            "margin_bottom": config["margin_bottom"],
            "margin_left": config["margin_left"],
            "margin_right": config["margin_right"],
        })

        font_size = self._calculate_font_size(config["font_size"])
        label_data = self._prepare_label_data(font_size)
        pages = self._prepare_pages(label_data)

        page_width = paperformat.page_width or 210
        page_height = paperformat.page_height or 297
        
        page_width = paperformat.page_width or 210
        page_height = paperformat.page_height or 297
        
        printable_width = float(page_width or 0) - float(config.get("margin_left") or 0) - float(config.get("margin_right") or 0)
        printable_height = float(page_height or 0) - float(config.get("margin_top") or 0) - float(config.get("margin_bottom") or 0)

        label_width = printable_width / self.cols if self.cols > 0 else 0
        label_height = printable_height / self.rows if self.rows > 0 else 0

        data = {
            "pages": pages,
            "rows": self.rows,
            "cols": self.cols,
            "printable_width": printable_width,
            "printable_height": printable_height,
            "label_width": label_width,
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

        report = self.env.ref("st_dynamic_product_label_print.action_report_product_labels")
        report.paperformat_id = temp_paperformat.id

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
