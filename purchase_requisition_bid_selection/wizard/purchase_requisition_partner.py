# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class PurchaseRequisitionPartner(models.TransientModel):
    _name = "purchase.requisition.partner"

    partner_id = fields.Char('partner id')

    @api.multi
    def create_order(self):
        ActWindow = self.env['ir.actions.act_window']
        Requisition = self.env['purchase.requisition']
        active_id = self.env.context and self.env.context.get('active_id', [])

        requisition = Requisition.browse(active_id)

        po_id = requisition.make_purchase_order(self.partner_id.id)[active_id]

        if not self.env.context.get('draft_bid', False):
            return {'type': 'ir.actions.act_window_close'}
        res = ActWindow.for_xml_id('purchase', 'purchase_rfq')
        res.update({'res_id': po_id,
                    'views': [(False, 'form')],
                    })
        return res
