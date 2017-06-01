# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class TestConsistentTypeAndState(common.TransactionCase):
    def test_all_approved_are_purchases(self):
        PO = self.env['purchase.order']
        self.assertFalse(PO.search([
            ('state', '=', 'approved'),
            ('type', '!=', 'purchase'),
        ]))
