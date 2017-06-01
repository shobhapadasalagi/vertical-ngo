# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class UpdateRemark(models.TransientModel):
    _name = "update.remark"

    def get_default_remark(self):
        ctx = self.env.context
        return self.env[ctx['active_model']].browse(ctx['active_id']).remark

    remark = fields.Text(default=get_default_remark)

    @api.multi
    def update_remark(self):
        self.ensure_one()
        ctx = self.env.context
        pol = self.env[ctx['active_model']].browse(ctx['active_id'])
        pol.remark = self.remark
        return {'type': 'ir.actions.act_window_close'}
