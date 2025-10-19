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

## Configuration

This module can be configured to match your specific label sheets and information requirements.

1.  Navigate to the main **Settings** menu in Odoo.
2.  On the **General Settings** page, find the **Product Label Printing** section.

You can customize the following options:

### Layout
-   **Number of Rows:** Define how many rows of labels are on a single page.
-   **Number of Columns:** Define how many columns of labels are on a single page.

> **Note:** This module uses a standard A4 paper format for the label sheet. To ensure your labels align correctly, you can adjust the page margins in the **Styling** section below.

### Content
-   **Show Internal Reference:** Check this to display the product's internal reference on the label.
-   **Show On-Hand Quantity:** Check this to display the current stock level.
-   **Show Attributes:** Check this to display the product's variant attributes (e.g., Color, Size).
-   **Show Barcode Digits:** Check this to display the numerical digits below the barcode image.

### Styling
-   **Base Font Size (px):** Set the base font size for the label text.
-   **Top/Bottom/Left/Right Margin (mm):** Adjust the margins of the page to ensure perfect alignment with your label sheets.

## Installation

1.  Copy the `st_dynamic_product_label_print` directory into the `addons` path of your Odoo instance.
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
