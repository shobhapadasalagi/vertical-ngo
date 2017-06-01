# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ActionModalAskValidity(models.TransientModel):
    _name = 'purchase.action_modal.ask_validity'
    _inherit = 'purchase.action_modal'

    validity = fields.Date("New end of validity", required=True)
