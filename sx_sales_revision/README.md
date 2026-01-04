# Sales Quotation/Order Revision

## Overview
The **Sales Quotation/Order Revision** module, developed by Spirix Software, enhances the Odoo Sales application by introducing the ability to revise sales quotations/orders and track their revision history. This feature is particularly useful for businesses that require a clear audit trail of changes made to sales orders over time.

## Key Features
- **Revision Tracking**: Allows users to create revisions of sales quotations/orders.
- **State Management**: Adds new states (`has_revision`, `revised`) to the sales order workflow.
- **Revision Family View**: Displays all revisions related to a sales order in a dedicated tab.
- **Enhanced Buttons**: Customizes the visibility of action buttons based on the state of the sales order.
- **Audit Trail**: Maintains a clear history of all revisions for better traceability.
- **Confirm Order**: On confirmation of any order other linked(Revised) order will be cancel.


## Installation
1. Ensure that the `sale_management` module is installed in your Odoo instance.
2. Copy the `sx_sales_revision` module folder into your Odoo addons directory.
3. Update the module list by navigating to **Apps** in the Odoo backend and clicking on **Update Apps List**.
4. Search for "Sales Quotation/Order Revision" in the Apps menu and install the module.

## Usage
### Creating a Revision
1. Open a sales quotation/order in the Odoo Sales module.
2. Ensure the order is in one of the following states: `sent`, `has_revision`, or `revised`.
3. Click the **Create Revision** button in the header.
4. A new sales order will be created as a revision of the current order.

### Viewing Revisions
1. Open a sales order with revisions.
2. Navigate to the **Sale Revisions** tab.
3. View the list of all related revisions, including details such as date, customer, salesperson, and state.

### Revision Count
- The revision count is displayed as a stat button in the sales order form view.
- Clicking the stat button will show all revisions in the order family.

## Technical Details
### Models
- **`sale.order`**: Extended to include fields for revision tracking:
  - `original_order_id`: Links to the original order.
  - `revised_order_ids`: One2many relation to track all revisions.
  - `revision_count`: Computed field to count the number of revisions.

### Views
- **Form View**: Enhanced to include:
  - A stat button for revision count.
  - A "Create Revision" button.
  - A new tab for displaying related revisions.
- **Button Visibility**: Action buttons are dynamically shown/hidden based on the state of the sales order.

### States
- Added new states to the sales order workflow:
  - `has_revision`: Indicates the order has revisions.
  - `revised`: Indicates the order is a revision of another order.

## License
This module is licensed under the Odoo Proprietary License v1.0 (OPL-1).

## Author
- **Company**: Spirix Software
- **Website**: [https://spirixsoftware.in/](https://spirixsoftware.in/)
- **Maintainer**: Spirix Software

For any inquiries or support, please write on spirixsoftware@zohomail.in
