# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class action_modal(models.TransientModel):
    _name = 'purchase.action_modal'

    @api.multi
    def action(self):
        for e in ('active_model', 'active_ids', 'action'):
            if e not in self._context:
                return False
        ctx = {'active_ids': self._ids,
               'active_id': self._ids[0]}
        model = self.env[self._context['active_model']]
        rec = model.browse(self._context['active_ids'])
        res = getattr(rec.with_context(ctx),
                      self._context['action'])()
        if isinstance(res, dict):
            return res
        return {'type': 'ir.actions.act_window_close'}


class action_modal_datetime(models.TransientModel):
    _name = 'purchase.action_modal.datetime'
    _inherit = 'purchase.action_modal'

    datetime = fields.Datetime('Date')
