# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

SELECTED_STATE = ('agreement_selected', 'Agreement selected')
AGR_SELECT = 'agreement_selected'


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Add workflow behavior"

    for_agreement = fields.Boolean('For Framework Agreement')
    agreement_expected_date = fields.Date('LTA expected valitidy period')
    agreement_promised_date = fields.Date('LTA promised valitidy period')

    def __init__(self, pool, cr):
        """Add a new state value using PO class property"""
        if SELECTED_STATE not in super(PurchaseOrder, self).STATE_SELECTION:
            super(PurchaseOrder, self).STATE_SELECTION.append(SELECTED_STATE)
        super(PurchaseOrder, self).__init__(pool, cr)

    @api.model
    def select_agreement(self, agr_id):
        """Pass PO in state 'Agreement selected'"""
        if isinstance(agr_id, (list, tuple)):
            assert len(agr_id) == 1
            agr_id = agr_id[0]
        return self.signal_workflow([agr_id], 'select_agreement')

    def po_tender_agreement_selected(self):
        """Workflow function that write state 'Agreement selected'"""
        return self.write({'state': AGR_SELECT})


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    _description = "Add make_agreement function"

    # Did you know a good way to supress SQL constraint to add
    # Python constraint...
    _sql_constraints = [('quantity_bid', 'CHECK(true)',
        'Selected quantity must be less or equal than the quantity in the bid'
    )]

    @api.multi
    def _check_quantity_bid(self):
        for line in self.browse():
            if line.order_id.framework_agreement_id:
                continue
            if (
                line.product_id.type == 'product' and
                not line.quantity_bid <= line.product_qty
            ):
                return False
        return True

    _constraints = [(
        _check_quantity_bid,
        'Selected quantity must be less or equal than the quantity in the bid',
        []
    )]

    @api.multi
    def _agreement_data(self, po_line, origin):
        """Get agreement values from PO line
        :param po_line: Po line records
        :returns: agreement dict to be used by orm.Model.create
        """
        portfolio_model = self.env['framework.agreement.portfolio']
        vals = {}
        vals['portfolio_id'] = portfolio_model.get_from_supplier(
            po_line.order_id.partner_id)[0]
        vals['product_id'] = po_line.product_id.id
        vals['quantity'] = po_line.product_qty
        vals['delay'] = po_line.product_id.seller_delay
        vals['origin'] = origin if origin else False
        return vals

    @api.multi
    def make_agreement(self, line_id, origin):
        """ generate a draft framework agreement
        :returns: a record of LTA
        """
        agr_model = self.env['framework.agreement']
        if isinstance(line_id, (list, tuple)):
            assert len(line_id) == 1
            line_id = line_id[0]
        current = self.browse(line_id)
        vals = self._agreement_data(current, origin)
        agr_id = agr_model.create(vals)
        return agr_model.browse(agr_id)
