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
        default=lambda self: self.env["ir.config_parameter"]
        .sudo()
        .get_param("st_dynamic_product_label_print.paperformat_id"),
    )
    rows = fields.Integer(
        string="Rows",
        default=lambda self: int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("st_dynamic_product_label_print.label_rows")
        ),
    )
    cols = fields.Integer(
        string="Columns",
        default=lambda self: int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("st_dynamic_product_label_print.label_cols")
        ),
    )
    skipped_pages = fields.Integer(
        string="Skip Full Pages",
        default=0,
        help="Number of full blank pages to print at the start (e.g., to advance printer after jam).",
    )
    start_row = fields.Integer(string="Start Row", default=1)
    start_col = fields.Integer(string="Start Column", default=1)

    @api.depends("product_ids", "label_quantity", "custom_quantity")
    def _compute_label_summary(self):
        for wizard in self:
            summary = []
            for product in wizard.product_ids:
                if wizard.label_quantity == "on_hand":
                    quantity = product.qty_available
                else:
                    quantity = wizard.custom_quantity
                quantity = max(quantity, 1)
                summary.append(f"{product.name}: {quantity} labels")
            wizard.label_summary = "\n".join(summary)

    label_summary = fields.Text(
        string="Label Summary", compute="_compute_label_summary"
    )

    def action_print_labels(self):
        self.ensure_one()
        if not self.product_ids:
            raise UserError(
                _("You need to select at least one product to print labels.")
            )

        # Validation for start position
        if self.start_row < 1 or self.start_row > self.rows:
            raise UserError(_("Start Row must be between 1 and %d.") % self.rows)
        if self.start_col < 1 or self.start_col > self.cols:
            raise UserError(_("Start Column must be between 1 and %d.") % self.cols)
        if self.skipped_pages < 0:
            raise UserError(_("Skipped Pages must be 0 or greater."))

        # Fetch configuration parameters
        get_param = self.env["ir.config_parameter"].sudo().get_param

        # Get base paperformat
        paperformat_id_param = get_param(
            "st_dynamic_product_label_print.paperformat_id"
        )
        if not paperformat_id_param or not paperformat_id_param.isdigit():
            raise UserError(
                _(
                    "The paper format is not configured. Please configure it in the settings."
                )
            )
        base_paperformat_id = int(paperformat_id_param)

        # Get dynamic margin values from settings
        margin_top = int(get_param("st_dynamic_product_label_print.label_margin_top"))
        margin_bottom = int(
            get_param("st_dynamic_product_label_print.label_margin_bottom")
        )
        margin_left = int(get_param("st_dynamic_product_label_print.label_margin_left"))
        margin_right = int(
            get_param("st_dynamic_product_label_print.label_margin_right")
        )

        # Create a temporary paper format with the dynamic margins.
        # This is the best practice to handle dynamic report layouts in Odoo.
        base_paperformat = self.env["report.paperformat"].browse(base_paperformat_id)
        temp_paperformat = base_paperformat.copy(
            {
                "name": f"Dynamic Label Paperformat - {self.id}",
                "margin_top": margin_top,
                "margin_bottom": margin_bottom,
                "margin_left": margin_left,
                "margin_right": margin_right,
            }
        )

        # --- Layout Calculation ---
        rows = self.rows
        cols = self.cols
        full_per_page = rows * cols

        # Get paper format dimensions and margins to calculate true printable area
        paperformat = self.paperformat_id
        if not paperformat:
            # If not set in wizard, get from config
            get_param = self.env["ir.config_parameter"].sudo().get_param
            paperformat_id_param = get_param(
                "st_dynamic_product_label_print.paperformat_id"
            )
            if paperformat_id_param and paperformat_id_param.isdigit():
                paperformat = self.env["report.paperformat"].browse(
                    int(paperformat_id_param)
                )

        if not paperformat:
            raise UserError(
                _(
                    "Please select a paper format in the wizard or set a default in the settings."
                )
            )

        page_width = paperformat.page_width or 210
        page_height = paperformat.page_height or 297
        margin_top = paperformat.margin_top
        margin_bottom = paperformat.margin_bottom
        margin_left = paperformat.margin_left
        margin_right = paperformat.margin_right

        printable_width = page_width - margin_left - margin_right
        printable_height = page_height - margin_top - margin_bottom

        # --- Dynamic Font Size Calculation ---
        initial_font_size = int(
            get_param("st_dynamic_product_label_print.label_font_size")
        )

        # --- Smart Scaling based on Area and Width ---
        base_rows, base_cols = 7.0, 2.0
        current_rows = self.rows if self.rows > 0 else base_rows
        current_cols = self.cols if self.cols > 0 else base_cols

        # 1. Calculate scaling based on area (good for overall size changes)
        base_label_area = (1 / base_rows) * (1 / base_cols)
        current_label_area = (1 / current_rows) * (1 / current_cols)
        # Using cube root (power of 0.33) to make scaling a bit more responsive
        area_scaling_factor = (
            (current_label_area / base_label_area) ** 0.33 if base_label_area > 0 else 1
        )

        # 2. Calculate scaling based on width (prevents overflow in narrow columns)
        # Using cube root (power of 0.33)
        width_scaling_factor = (
            (base_cols / current_cols) ** 0.33 if current_cols > 0 else 1
        )

        # 3. Add a direct scaling factor for rows to be more aggressive
        # Using square root (power of 0.5)
        row_scaling_factor = (
            (base_rows / current_rows) ** 0.5 if current_rows > 0 else 1
        )

        # 4. Use the smaller of the three factors to be safe
        final_scaling_factor = min(
            area_scaling_factor, width_scaling_factor, row_scaling_factor
        )
        final_font_size = initial_font_size * final_scaling_factor

        label_data = []
        for product in self.product_ids:
            quantity = (
                product.qty_available
                if self.label_quantity == "on_hand"
                else self.custom_quantity
            )
            quantity = max(int(quantity), 1)

            attribute_string = " ".join(
                product.product_template_attribute_value_ids.mapped("name")
            )

            for i in range(quantity):
                label_data.append(
                    {
                        "product_name": product.name,
                        "attribute_string": attribute_string,
                        "default_code": product.default_code or "",
                        "barcode": product.barcode or "",
                        "sequence": i + 1,
                        "total_quantity": quantity,
                        "on_hand_qty": product.qty_available,
                        "font_size": final_font_size,
                    }
                )

        # --- Fixed Offset and Paging Logic ---
        offset = (self.start_row - 1) * cols + (self.start_col - 1)
        first_page_size = full_per_page - offset

        # First page: empties + labels to fill it
        first_page_labels = ([{}] * offset) + label_data[:first_page_size]
        pages = [first_page_labels]

        # Remaining labels: chunk into full (or partial) pages
        remaining_labels = label_data[first_page_size:]
        i = 0
        while i < len(remaining_labels):
            page_size = min(full_per_page, len(remaining_labels) - i)
            pages.append(remaining_labels[i : i + page_size])
            i += full_per_page

        # --- Add Skipped Full Blank Pages at Start ---
        blank_page = [{}] * full_per_page
        for _ in range(self.skipped_pages):
            pages.insert(0, blank_page)

        data = {
            "pages": pages,
            "rows": rows,
            "cols": cols,
            "printable_width": printable_width,
            "printable_height": printable_height,
            "show_barcode_digits": get_param(
                "st_dynamic_product_label_print.label_show_barcode_digits"
            )
            == "True",
            "show_internal_ref": get_param(
                "st_dynamic_product_label_print.label_show_internal_ref"
            )
            == "True",
            "show_on_hand_qty": get_param(
                "st_dynamic_product_label_print.label_show_on_hand_qty"
            )
            == "True",
            "show_stock_label": get_param(
                "st_dynamic_product_label_print.label_show_stock_label"
            )
            == "True",
            "show_attributes": get_param(
                "st_dynamic_product_label_print.label_show_attributes"
            )
            == "True",
        }

        # Get the report action and generate the PDF using the temporary paperformat
        report = self.env.ref(
            "st_dynamic_product_label_print.action_report_product_labels"
        )
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
