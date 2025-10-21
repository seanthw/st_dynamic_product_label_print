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
    rows = fields.Integer(string="Rows", default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('st_dynamic_product_label_print.label_rows', 7)))
    cols = fields.Integer(string="Columns", default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('st_dynamic_product_label_print.label_cols', 2)))

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
            raise UserError(_("You need to select at least one product to print labels."))

        # Fetch configuration parameters
        get_param = self.env['ir.config_parameter'].sudo().get_param
        
        # Get base paperformat
        paperformat_id_param = get_param('st_dynamic_product_label_print.paperformat_id')
        base_paperformat_id = int(paperformat_id_param) if paperformat_id_param and paperformat_id_param.isdigit() else False
        
        if not base_paperformat_id:
            # Fallback to a default if not configured
            paperformat_ref = self.env.ref('stock.paperformat_label_sheet_a4', raise_if_not_found=False)
            if not paperformat_ref:
                raise UserError(_("No default paper format found. Please ensure the 'stock' module is installed or configure a base paper format in the settings."))
            base_paperformat_id = paperformat_ref.id

        # Get dynamic margin values from settings
        margin_top = int(get_param('st_dynamic_product_label_print.label_margin_top', 5))
        margin_bottom = int(get_param('st_dynamic_product_label_print.label_margin_bottom', 5))
        margin_left = int(get_param('st_dynamic_product_label_print.label_margin_left', 5))
        margin_right = int(get_param('st_dynamic_product_label_print.label_margin_right', 5))

        # Create a temporary paper format with the dynamic margins.
        # This is the best practice to handle dynamic report layouts in Odoo.
        base_paperformat = self.env['report.paperformat'].browse(base_paperformat_id)
        temp_paperformat = base_paperformat.copy({
            'name': f'Dynamic Label Paperformat - {self.id}',
            'margin_top': margin_top,
            'margin_bottom': margin_bottom,
            'margin_left': margin_left,
            'margin_right': margin_right,
        })
        
        # --- Dynamic Font Size Calculation ---
        initial_font_size = int(get_param('st_dynamic_product_label_print.label_font_size', 12))
        
        # Baseline layout dimensions (e.g., 7 rows, 2 columns)
        base_rows, base_cols = 7.0, 2.0
        base_label_area = (1 / base_rows) * (1 / base_cols)
        
        # Current layout dimensions
        current_rows = self.rows if self.rows > 0 else base_rows
        current_cols = self.cols if self.cols > 0 else base_cols
        current_label_area = (1 / current_rows) * (1 / current_cols)
        
        # Calculate font size scaling factor based on the change in area.
        scaling_factor = math.sqrt(current_label_area / base_label_area) if base_label_area > 0 else 1
        final_font_size = initial_font_size * scaling_factor

        label_data = []
        for product in self.product_ids:
            quantity = product.qty_available if self.label_quantity == 'on_hand' else self.custom_quantity
            quantity = max(int(quantity), 1)
            
            attribute_string = " ".join(
                product.product_template_attribute_value_ids.mapped("name")
            )

            for i in range(quantity):
                label_data.append({
                    'product_name': product.name,
                    'attribute_string': attribute_string,
                    'default_code': product.default_code or '',
                    'barcode': product.barcode or '',
                    'sequence': i + 1,
                    'total_quantity': quantity,
                    'on_hand_qty': product.qty_available,
                    'font_size': final_font_size,
                })

        # Chunk labels into pages
        labels_per_page = self.rows * self.cols
        pages = [label_data[i:i + labels_per_page] for i in range(0, len(label_data), labels_per_page)]

        data = {
            'pages': pages,
            'rows': self.rows,
            'cols': self.cols,
            'show_barcode_digits': get_param('st_dynamic_product_label_print.label_show_barcode_digits') == 'True',
            'show_internal_ref': get_param('st_dynamic_product_label_print.label_show_internal_ref') == 'True',
            'show_on_hand_qty': get_param('st_dynamic_product_label_print.label_show_on_hand_qty') == 'True',
            'show_attributes': get_param('st_dynamic_product_label_print.label_show_attributes') == 'True',
        }
        
        # Get the report action and generate the PDF using the temporary paperformat
        report = self.env.ref('st_dynamic_product_label_print.action_report_product_labels')
        report.paperformat_id = temp_paperformat.id

        report_action = report.report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        
        return report_action
