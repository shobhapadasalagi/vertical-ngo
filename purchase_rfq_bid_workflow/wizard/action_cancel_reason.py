# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ActionModalCancelReason(models.TransientModel):
    _name = 'purchase.action_modal.cancel_reason'
    _inherit = 'purchase.action_modal'

    reason_id = fields.Many2one(
        'purchase.cancel_reason', 'Reason for Cancellation', required=True)
