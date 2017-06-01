# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    origin_address_id = fields.Many2one('res.partner', string='Origin Address',
        readonly=True,
        compute='_origin_address',
        help='The place from which the shipment will be sent')

    @api.depends('order_id.warehouse_id',
                 'route_id',
                 'order_id.company_id.partner_id')
    @api.one
    def _origin_address(self):
        if self.route_id:
            address = self.env['res.partner']
        elif self.order_id.warehouse_id.partner_id:
            address = self.order_id.warehouse_id.partner_id
        else:
            address = self.order_id.company_id.partner_id
        self.origin_address_id = address


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    LO_STATES = {
        'cancel': [('readonly', True)],
        'progress': [('readonly', True)],
        'manual': [('readonly', True)],
        'shipping_except': [('readonly', True)],
        'invoice_except': [('readonly', True)],
        'done': [('readonly', True)],
    }

    consignee_id = fields.Many2one(
        'res.partner',
        string='Consignee',
        states=LO_STATES,
        domain=[('is_consignee', '=', True)],
        help="The person to whom the shipment is to be delivered.")

    @api.model
    def _prepare_procurement_group(self, order):
        res = super(SaleOrder, self)._prepare_procurement_group(order)
        res.update({'consignee_id': order.consignee_id.id,
                    'delivery_address_id': order.partner_shipping_id.id,
                    'partner_id': order.partner_id.id,
                    })
        return res

    @api.model
    def _prepare_order_line_procurement(self, order, line, group_id=False):
        res = super(SaleOrder, self)._prepare_order_line_procurement(
            order, line, group_id)
        res['origin_address_id'] = line.origin_address_id.id
        return res
