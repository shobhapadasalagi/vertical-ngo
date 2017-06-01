# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details

{"name": "Purchase Requisition Auto RFQ",
 "summary": "Automatically create RFQ from a purchase requisition",
 "version": "10.0.1.0.0",
 "author": "Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.",
 "category": "Purchase Management",
 "license": "AGPL-3",
 'complexity': "normal",
 "images": [],
 "description": """
Purchase Requisition Auto RFQ
=============================
This module adds a button on the purchase requisition form to create a RFQ
using the suppliers from the products listed in the requisition.
Note: nose is required to run the tests. It is not listed as en external
dependency because it is not needed in production.
""",
 "depends": [
             "purchase_requisition",
            ],
    "data": [
             "view/purchase_requisition.xml",
            ],
    "auto_install": False,
    "installable": True,
 }
