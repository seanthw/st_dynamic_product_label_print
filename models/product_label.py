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

        data = {'labels': label_data}
        
        # Get the report action and generate the PDF
        report_action = self.env.ref('st_dynamic_product_label_print.action_report_product_labels').report_action(None, data=data)
        report_action.update({'close_on_report_download': True})
        return report_action
