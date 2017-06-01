# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ActionModalAskSelectionReasons(models.TransientModel):
    _name = 'purchase.action_modal.ask_selection_reasons'
    _inherit = 'purchase.action_modal'

    selection_reasons = fields.Text(required=True)
