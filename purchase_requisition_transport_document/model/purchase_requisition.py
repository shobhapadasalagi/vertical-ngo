# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    transport_document_ids = fields.Many2many(
        'transport.document',
        string="Transport Documents"
    )

    @api.model
    def _prepare_purchase_order(self, requisition, supplier):
        """Propagate transport documents from tender to RFQ"""

        values = super(PurchaseRequisition, self
                       )._prepare_purchase_order(requisition, supplier)
        values.update({
            'transport_document_ids': [
                (4, doc.id) for doc in requisition.transport_document_ids
            ],
        })
        return values
