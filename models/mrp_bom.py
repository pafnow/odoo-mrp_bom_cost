# Copyright 2020 Pafnow

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    cost_price = fields.Float('Cost Price', compute='_get_costs', digits='Product Price')
    cost_total = fields.Float('Total Cost', compute='_get_costs', digits='Product Price')

    @api.depends('product_id', 'product_qty')
    def _get_costs(self):
        for record in self:
            if not record.product_id:
                return {}
            else:
                record.cost_price = record.product_id.standard_price
                record.cost_total = record.product_id.standard_price * record.product_qty / record.bom_id.product_qty


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    cost_bom = fields.Float('BOM Cost', compute='_get_cost_bom', digits='Product Price', help='Total BOM Cost for 1 produced quantity')

    @api.depends('bom_line_ids.cost_total')
    def _get_cost_bom(self):
        for record in self:
            total = 0.0
            for line in record.bom_line_ids:
                total += line.cost_total
            record.cost_bom = total/record.product_qty
