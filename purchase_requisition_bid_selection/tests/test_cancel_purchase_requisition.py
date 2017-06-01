# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import odoo.tests.common as common


class test_cancel_purchase_requisition(common.TransactionCase):
    """ Test the cancellation of purchase requisition and ensure that related
    Purchase Orders/Request For Quotation are cancelled
    """

    def setUp(self):
        super(test_cancel_purchase_requisition, self).setUp()
        PReq = self.env['purchase.requisition']
        PO = self.env['purchase.order']

        self.preq = PReq.new({'state': 'draft'})

        self.po_sent = PO.new({'state': 'draft'})
        self.po_draft = PO.new({'state': 'sent'})

    def test_cancel_draft_purchase_requisition(self):
        """ We cancel a draft purchase requisition
        """
        self.preq.tender_cancel()
        self.assertEqual(self.preq.state, 'cancel')

    def test_cancel_in_progress_purchase_requisition_without_bid(self):
        """ We cancel a confirmed purchase requisition without Bid
        """
        self.preq.tender_cancel()
        self.assertEqual(self.preq.state, 'cancel')

    def test_cancel_in_progress_purchase_requisition_with_1draft_rfq(self):
        """ We cancel a confirmed purchase requisition with 1 RFQ in
        draft state
        """
        self.preq.state = 'in_progress'
        self.purchase_ids = self.po_draft
        self.preq.tender_cancel()
        for po in self.preq.purchase_ids:
            self.assertEquals(po.state, 'cancel')

    def test_cancel_in_progress_purchase_requisition_with_1sent_rqf(self):
        """ We cancel a confirmed purchase requisition with 1 RFQ
        in sent state
        """
        self.preq.state = 'in_progress'
        self.purchase_ids = self.po_sent
        self.preq.tender_cancel()
        self.assertEqual(self.preq.state, 'cancel')
        for po in self.preq.purchase_ids:
            self.assertEquals(po.state, 'cancel')

    def test_cancel_in_progress_purchase_requisition_with_2bids(self):
        """ We cancel a confirmed purchase requisition with 2 RFQ
        """
        purchases = self.env['purchase.order']
        purchases |= self.po_draft
        purchases |= self.po_sent
        self.preq.state = 'in_progress'
        self.preq.tender_cancel()
        self.assertEqual(self.preq.state, 'cancel')
        for po in self.preq.purchase_ids:
            self.assertEquals(po.state, 'cancel')
