# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, exceptions
from odoo.tools.translate import _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin_address_id = fields.Many2one('res.partner','Origin Address')
    consignee_id = fields.Many2one(
        'res.partner', 'Consignee',
        domain=[('is_consignee', '=', True)],
        help="The person to whom the shipment is to be delivered.")

    @api.onchange('dest_address_id')
    def new_onchange_dest_address_id(self):
        """Find a picking type from the address
        If the address can be an internal warehouse or a customer, the picking
        type is changed accordingly. This intentionally overrides the original
        without super, and should be consistent with the module
        purchase_requisition_transport_multi_address.
        A similar logic to choose the picking type is used in the module
        framework_agreement_sourcing in github.com/OCA/vertical-ngo.
        """
        PickType = self.env['stock.picking.type']
        types = PickType.search([
            ('warehouse_id.partner_id', '=', self.dest_address_id.id),
            ('code', '=', 'incoming')])

        if types:
            if self.picking_type_id in types:
                return
            picking_type = types[0]
        elif self.dest_address_id.customer:
            # if destination is not for a warehouse address,
            # we set dropshipping picking type
            ref = 'stock_dropshipping.picking_type_dropship'
            picking_type = self.env.ref(ref)
        else:
            raise exceptions.Warning(
                _('The delivery address %s is not the address of a '
                  'warehouse or the address of a customer.') %
                self.dest_address_id.name)
        self.picking_type_id = picking_type

    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        """If the picking type has an address, use it.

        Do not empty the address none is found, because that gives a
        short circuit with the onchange of the address.
        """

        if self.picking_type_id:
            pick_type = self.picking_type_id

            if pick_type.warehouse_id.partner_id:
                self.dest_address_id = pick_type.warehouse_id.partner_id.id

            if pick_type.default_location_dest_id:
                self.location_id = pick_type.default_location_dest_id
                self.related_location_id = pick_type.default_location_dest_id
                self.related_usage = pick_type.default_location_dest_id.usage

    @api.multi
    def onchange_partner_id(self, partner_id):
        res = super(PurchaseOrder, self).onchange_partner_id(partner_id)
        res['value']['origin_address_id'] = partner_id
        return res

    @api.multi
    def action_picking_create(self):
        res = super(PurchaseOrder, self).action_picking_create()
        for order in self:
            order.picking_ids.write({
                'partner_id': order.partner_id.id,
                'delivery_address_id': order.dest_address_id.id,
                'origin_address_id': order.origin_address_id.id,
                'consignee_id': order.consignee_id.id,
            })
        return res

    @api.model
    def _prepare_order_line_move(self,
                                 order,
                                 order_line,
                                 picking_id,
                                 group_id):
        """modify the group to add the addresses"""
        group = self.env['procurement.group'].browse(group_id)
        fields = {}
        if not group.consignee_id:
            fields['consignee_id'] = order.consignee_id.id
        if not group.delivery_address_id:
            fields['delivery_address_id'] = order.dest_address_id.id
        if not group.origin_address_id:
            fields['origin_address_id'] = order.origin_address_id.id
        if fields:
            group.write(fields)
        return super(PurchaseOrder, self)._prepare_order_line_move(order,
                                                                   order_line,
                                                                   picking_id,
                                                                   group_id)
