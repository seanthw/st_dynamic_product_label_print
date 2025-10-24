# [2.1.0](https://github.com/seanthw/st_dynamic_product_label_print/compare/v2.0.0...v2.1.0) (2025-10-24)


### Features

* **labels:** Overhaul label printing for uniformity and control ([#4](https://github.com/seanthw/st_dynamic_product_label_print/issues/4)) ([29be180](https://github.com/seanthw/st_dynamic_product_label_print/commit/29be18089d64bd6b2a69c02d5aa11c3a43f209a4)), closes [hi#density](https://github.com/hi/issues/density)

# [2.0.0](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.6...v2.0.0) (2025-10-22)


### Features

* Centralized Configuration and Dynamic Label Generation ([#3](https://github.com/seanthw/st_dynamic_product_label_print/issues/3)) ([3bbd25f](https://github.com/seanthw/st_dynamic_product_label_print/commit/3bbd25ffd29b8870b11f6fc1bb3f94cac1b74af1))


### BREAKING CHANGES

* The paper format is now configured in the general settings instead of the print wizard.

* fix(report): ensure dynamic paper format persists for rendering

The previous implementation prematurely deleted the temporary paper format record before the report rendering process could use it, causing a race condition and resulting in incorrect layouts. This commit removes the faulty cleanup logic, ensuring the dynamically generated paper format is available when the PDF is created.

* feat: Implement multi-page label printing

The label generation logic has been updated to support multi-page printing. The 'action_print_labels' method now chunks labels into pages, and the QWeb template iterates through these pages to render them correctly.

* fix(style): Vertically center label content using flexbox

The previous vertical alignment fix was not working as expected. This commit uses CSS flexbox to properly center the content within the label, ensuring that it is not cut off during printing.

* fix(style): Add responsive font size for long product names

The font size for the product name is now dynamically adjusted based on its length. If the name is longer than 25 characters, the font size is reduced to prevent the text from overflowing the label's boundaries.

* fix(style): Implement proportional font scaling for all text

The font size for the entire label is now calculated based on the label's area (width and height). This ensures all text elements scale proportionally, improving readability and layout consistency across different row/column configurations.

* feat(style): Increase font size for barcode digits and label info

The font sizes for the barcode digits and the secondary label information have been increased to improve readability.

* feat: Enable barcode digits by default

* style: Indent reports.xml

* refactor(config): Centralize and correct default settings

* docs: Update configuration instructions

## [1.1.6](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.5...v1.1.6) (2025-10-19)


### Bug Fixes

* **versioning:** correct version update script ([02a7846](https://github.com/seanthw/st_dynamic_product_label_print/commit/02a784670a228fd9258e1376d933d7043aeb0c1b))

## [1.1.5](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.4...v1.1.5) (2025-10-19)


### Bug Fixes

* **ci:** use correct release script and configuration ([688f819](https://github.com/seanthw/st_dynamic_product_label_print/commit/688f81975e4c5744ac4256db6ba8b93b4ce3e9b6))

## [1.1.4](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.3...v1.1.4) (2025-10-18)


### Bug Fixes

* **ci:** remove incorrect pkgRoot from release config ([bf13f05](https://github.com/seanthw/st_dynamic_product_label_print/commit/bf13f0596c399d2de8fa1c5fad33d53cfb3036ec))

## [1.1.3](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.2...v1.1.3) (2025-10-18)


### Bug Fixes

* **ci:** restore correct pkgRoot for semantic-release ([9ace5a0](https://github.com/seanthw/st_dynamic_product_label_print/commit/9ace5a04fbdb78d0b407f747a72ac51ea2fce548))

## [1.1.2](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.1...v1.1.2) (2025-10-18)


### Bug Fixes

* **ci:** correctly configure git plugin to commit manifest ([fdfbe01](https://github.com/seanthw/st_dynamic_product_label_print/commit/fdfbe0197557f4747ef0bbd70689c8d34414d644))

## [1.1.1](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.1.0...v1.1.1) (2025-10-18)


### Bug Fixes

* **ci:** persist credentials for semantic-release ([d0d15dd](https://github.com/seanthw/st_dynamic_product_label_print/commit/d0d15dd6b01a2a2b19a4d6ee95d09c7e15618d3b))

# [1.1.0](https://github.com/seanthw/st_dynamic_product_label_print/compare/v1.0.0...v1.1.0) (2025-10-18)


### Features

* add configurable label printing and paper format selection ([eaf5a98](https://github.com/seanthw/st_dynamic_product_label_print/commit/eaf5a9831835162d520a2c2db8cc97cf286cec04))

# 1.0.0 (2025-10-18)


### Bug Fixes

* **deps:** ensure paperformat is loaded before reports ([1b966a0](https://github.com/seanthw/st_dynamic_product_label_print/commit/1b966a0c3ba805fc0fd1c9e713c0c0d753a2ac40))
* Ensure correct view loading order on install ([8ab4796](https://github.com/seanthw/st_dynamic_product_label_print/commit/8ab47960a1eb50fe864d2f55de295f8b2496c94f))
* Resolve installation and runtime errors for Odoo 18 ([6b0446d](https://github.com/seanthw/st_dynamic_product_label_print/commit/6b0446dd98768dbcc131f2be8f988d5f9ea5f14a))
* Use standard Odoo barcode widget to render images ([48bc0f3](https://github.com/seanthw/st_dynamic_product_label_print/commit/48bc0f351a9925256408d2243bec5f83eb5bf9cf))


### Features

* add .gitignore ([a0d6cb9](https://github.com/seanthw/st_dynamic_product_label_print/commit/a0d6cb97888643f2f045b86ef4c5f665eaba6b01))
* add configurable label printing and paper format selection ([ffe763a](https://github.com/seanthw/st_dynamic_product_label_print/commit/ffe763ad62c29bbe88c085c9919757c32338936b))
