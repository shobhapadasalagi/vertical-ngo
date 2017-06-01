# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from itertools import chain
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
#from odoo.purchase import AGR_SELECT as PO_AGR_SELECT

SELECTED_STATE = ('agreement_selected', 'Agreement selected')
AGR_SELECT = 'agreement_selected'


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.multi
    def open_wizard_confirm_generate_agreement(self):
        view = self.env.ref(
            'framework_agreement_requisition.'
            'confirm_generate_agreement_form_view'
        )
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'confirm.generate.agreement',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'target': 'new',
            'context': self.env.context,
        }

    @api.model
    def _prepare_purchase_order(self, requisition, supplier):
        _super = super(PurchaseRequisition, self)
        values = _super._prepare_purchase_order(requisition,
                                                supplier)
        values.update(
            {'for_agreement': requisition.framework_agreement_tender,
             'agreement_expected_date': requisition.agreement_end_date,
             })
        return values


class PurchaseRequisitionClassic(models.Model):
    _inherit = "purchase.requisition"
    _description = "Add support to negociate LTA using tender process"

#    def __init__(self, pool, cr):
#        """Nasty hack to add fields to select fields
#        We do this in order not to compromising other state added
#        by other addons that are not in inheritance chain...
#        """
#        sel = super(PurchaseRequisitionClassic, self).__str__['state']
#        if SELECTED_STATE not in sel.selection:
#            sel.selection.append(SELECTED_STATE)
#        super(PurchaseRequisitionClassic, self).__init__(pool, cr)

#    def __init__(self, pool, cr):
#        """Nasty hack to add fields to select fields
#        We do this in order not to compromising other state added
#        by other addons that are not in inheritance chain...
#        """
#        sel = super(PurchaseRequisitionClassic, self).__str__('state')
#        if SELECTED_STATE not in sel.selection:
#            sel.selection.append(SELECTED_STATE)
#        super(PurchaseRequisitionClassic, self).__init__(pool, cr)

    #    def __init__(self, pool, cr):
#        """Nasty hack to add fields to select fields
#        We do this in order not to compromising other state added
#        by other addons that are not in inheritance chain...
#        """
#        sel = super(PurchaseRequisitionClassic, self)._columns['state']
#        if SELECTED_STATE not in sel.selection:
#            sel.selection.append(SELECTED_STATE)
#        super(PurchaseRequisitionClassic, self).__init__(pool, cr)
#
#    def __getattr__(self, sel):
#        return self(sel)

    framework_agreement_tender = fields.Boolean('Negociate Agreement')
    agreement_end_date = fields.Date('LTA expected valitidy period')

    @api.multi
    def tender_agreement_selected(self):
        """Workflow function that write state 'Agreement selected'"""
        return self.write({'state': AGR_SELECT})

    @api.multi
    def select_agreement(self, agr_id):
        """Pass tender to state 'Agreement selected'"""
        if isinstance(agr_id, (list, tuple)):
            assert len(agr_id) == 1
            agr_id = agr_id[0]
        return self.signal_workflow([agr_id], 'select_agreement')

    @api.multi
    def _agreement_selected(self):
        """Tells tender that an agreement has been selected"""
        if isinstance((int, long)):
            generated = []
            for req in self.browse():
                if not req.framework_agreement_tender:
                    raise ValidationError(_('Invalid tender'),
                                        _('Request is not of type agreement'))
                self.select_agreement(req.id)
                req.refresh()
                if req.state != AGR_SELECT:
                    raise RuntimeError('requisition %s does not pass to state'
                                       ' agreement_selected' %
                                       req.name)
                rfqs = chain.from_iterable(req_line.purchase_line_ids
                                           for req_line in req.line_ids)
                po_to_select = []
                po_to_cancel = []
                for rfq in rfqs:
                    if rfq.state == 'confirmed':
                        agr_record = rfq.make_agreement(rfq.id, req.name)
                        generated.append(agr_record)
                        po_to_select.append(rfq.order_id)
                    else:
                        po_to_cancel.append(rfq.order_id)
                if not po_to_select:
                    raise ValidationError(_('No confirmed RFQ related to \
                                            tender'),
                                         _('Please choose at least one'))
                for p_order in set(po_to_select):
                    p_order.select_agreement()
                    p_order.refresh()
                    if p_order.state != AGR_SELECT:
                        raise RuntimeError(
                            'Purchase order %s does not pass to %s' %
                            (p_order.name, AGR_SELECT))
                for p_order in set(po_to_cancel):
                    self.signal_workflow([p_order.id], 'purchase_cancel')
        return generated

    @api.multi
    def agreement_selected(self):
        agrements = self._agreement_selected()
        a_ids = [x.id for x in agrements]
        return {
            'name': _('Generated Agreements'),
            'view_mode': 'tree,form',
            'res_model': 'framework.agreement',
            'domain': [('id', 'in', a_ids)],
            'target': 'current',
            'view_id': False,
            'context': {},
            'type': 'ir.actions.act_window',
        }
