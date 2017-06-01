# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    transport_document_ids = fields.Many2many(
        'transport.document',
        string="Transport Documents"
    )
