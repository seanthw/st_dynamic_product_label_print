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
        
        label_rows = self.rows
        label_cols = self.cols
        paperformat_id_param = get_param('st_dynamic_product_label_print.paperformat_id')
        paperformat_id = int(paperformat_id_param) if paperformat_id_param and paperformat_id_param.isdigit() else False
        
        # Prepare data for the report
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
                })

        data = {
            'labels': label_data,
            'rows': label_rows,
            'cols': label_cols,
            'show_barcode_digits': get_param('st_dynamic_product_label_print.label_show_barcode_digits') == 'True',
            'show_internal_ref': get_param('st_dynamic_product_label_print.label_show_internal_ref') == 'True',
            'show_on_hand_qty': get_param('st_dynamic_product_label_print.label_show_on_hand_qty') == 'True',
            'show_attributes': get_param('st_dynamic_product_label_print.label_show_attributes') == 'True',
            'font_size': int(get_param('st_dynamic_product_label_print.label_font_size', 12)),
            'margin_top': int(get_param('st_dynamic_product_label_print.label_margin_top', 5)),
            'margin_bottom': int(get_param('st_dynamic_product_label_print.label_margin_bottom', 5)),
            'margin_left': int(get_param('st_dynamic_product_label_print.label_margin_left', 5)),
            'margin_right': int(get_param('st_dynamic_product_label_print.label_margin_right', 5)),
        }
        
        # Get the report action and generate the PDF
        report = self.env.ref('st_dynamic_product_label_print.action_report_product_labels')
        if paperformat_id:
            report.paperformat_id = paperformat_id

        report_action = report.report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action
