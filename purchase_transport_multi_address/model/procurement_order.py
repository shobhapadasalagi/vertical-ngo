# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def create_procurement_purchase_order(self,
                                          procurement,
                                          po_vals,
                                          line_vals):
        po_vals.update({'consignee_id': procurement.consignee_id.id,
                        'origin_address_id': po_vals['partner_id'],
                        })
        _super = super(ProcurementOrder, self)
        return _super.create_procurement_purchase_order(procurement,
                                                        po_vals,
                                                        line_vals)
