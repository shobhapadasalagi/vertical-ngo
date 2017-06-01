# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class UpdateBidInternalRemark(models.TransientModel):
    _name = "update.bid.internal.remark"

    def get_default_remark(self):
        ctx = self.env.context
        po = self.env[ctx['active_model']].browse(ctx['active_id'])
        return po.bid_internal_remark

    bid_internal_remark = fields.Text(default=get_default_remark)

    @api.multi
    def update_remark(self):
        self.ensure_one()
        ctx = self.env.context
        po = self.env[ctx['active_model']].browse(ctx['active_id'])
        po.bid_internal_remark = self.bid_internal_remark
        return {'type': 'ir.actions.act_window_close'}
