# Dynamic Product Label Print

## Overview

This Odoo module provides a flexible way to print product labels directly from the Odoo interface. It is designed to work primarily with **Product Variants**, as these are the actual, stockable items in your inventory that have unique barcodes and on-hand quantities.

The module allows users to generate labels for single or multiple product variants, with the quantity based on either the current on-hand stock or a custom user-defined amount. For convenience, a shortcut is also provided on the main Product Template form to print labels for all of its variants at once.

The generated labels are formatted in a clean, two-column layout and include essential product information, such as the product name, variant attributes, internal reference, and a Code128 barcode.

## Features

- **Variant-Focused Logic:** Correctly bases labels on product variants, which hold the specific stock and barcode information.
- **Dynamic Quantity:** Choose to print labels based on:
    - Current "On Hand" quantity.
    - A custom quantity entered by the user.
- **Multiple Variant Selection:** Print labels for multiple, specific product variants at once from the list view.
- **Print All Variants:** Use the shortcut on a Product Template to print labels for all its associated variants.
- **Informative Layout:** Each label is clearly formatted to display:
    - Product Name
    - Product Attributes (e.g., Color, Size)
    - Internal Reference (Code)
    - Barcode Image (Code128)
    - Current Stock Level
    - Label sequence number (e.g., Label 1 of 10)
- **Clean PDF Output:** Generates a professional, easy-to-read PDF document with labels arranged in a two-column grid.

## Installation

1.  Copy the `bi_dynamic_product_label_print` directory into the `addons` path of your Odoo instance.
2.  Navigate to the **Apps** menu in Odoo.
3.  Click on **Update Apps List**.
4.  Search for "Dynamic Product Label Print" and click the **Install** button.

## Usage

There are two primary ways to print labels:

### Method 1: Printing Specific Product Variants

This is the most common method for printing labels for specific items.

1.  Navigate to the **Inventory** module.
2.  Go to **Products -> Product Variants**.
3.  In the list view, select the checkboxes next to the variants you wish to print labels for.
4.  Click the **Action** button that appears at the top of the list.
5.  Select **Print Labels** from the dropdown menu.
6.  In the wizard that appears, choose your desired quantity type and click **Print Labels**.

### Method 2: Printing All Variants of a Product (Shortcut)

This method is a convenient shortcut to print labels for all variants belonging to a single product template.

1.  Navigate to the **Inventory** module.
2.  Go to **Products -> Products**.
3.  Open the form view of the main product template.
4.  Click the **Print Labels** button located in the button box at the top of the form.
5.  The wizard will open, pre-filled with all variants of that product. Choose your quantity type and click **Print Labels**.

## Author

Sean Thawe

## License

LGPL-3
