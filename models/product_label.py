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
            raise UserError(_("Please select at least one product."))

        # Prepare label data
        labels = []
        for product in self.product_ids:
            if self.label_quantity == "on_hand":
                quantity = product.qty_available
            else:
                quantity = self.custom_quantity

            quantity = max(int(quantity), 1)

            for i in range(quantity):
                labels.append(
                    {
                        "product_id": product.id,
                        "product_name": product.name,
                        "default_code": product.default_code or "",
                        "barcode": product.barcode or "",
                        "sequence": i + 1,
                        "total_quantity": quantity,
                        "on_hand_qty": product.qty_available,
                    }
                )

        # Pass data to report
        return self.env.ref(
            "bi_dynamic_product_label_print.action_report_product_labels"
        ).report_action(self, data={"labels": labels})
