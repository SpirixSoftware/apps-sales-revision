# -*- coding: utf-8 -*-
# Copyright (C) 2025 Spirix Software
# This file is part of a proprietary Odoo addon developed by Spirix Software
# License OPL-1 (Odoo Proprietary License v1.0)

from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.addons.sale.models.sale_order import SALE_ORDER_STATE

SALE_ORDER_STATE.insert(2, ("has_revision", "Has Revisions"))
SALE_ORDER_STATE.insert(3, ("revised", "Revised Order"))


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=SALE_ORDER_STATE)
    original_order_id = fields.Many2one("sale.order", string="Origin")
    revised_order_ids = fields.One2many("sale.order", "original_order_id", string="Revisions")
    revision_count = fields.Integer(
        string="Revision Count",
        compute="_compute_revision_count",
        store=True)


    def _compute_revision_count(self):
        for rec in self:
            rec.revision_count = len(rec._get_full_revision_family())

    def _recompute_revision_count_family(self):
        for rec in self:
            family = rec._get_full_revision_family()
            family._compute_revision_count()

    def _confirmation_error_message(self):
        """
            Overwrite base method to confirm sale order from revised and has_revision state.
        """
        self.ensure_one()
        if self.state not in {"draft", "has_revision", "sent", "revised"}:
            return _("Some orders are not in a state requiring confirmation.")
        if any(
                not line.display_type and not line.is_downpayment and not line.product_id
                for line in self.order_line
        ):
            return _("A line on these orders missing a product, you cannot confirm it.")

        return False

    def action_create_revision(self):
        """Action to create a revised sale order."""
        self.ensure_one()
        revision_count = len(self.revised_order_ids) + 1
        revised_order_name = f"R{str(revision_count).zfill(2)}_{self.name}"
        vals = {
            'name': revised_order_name,
            'state': 'revised',
            'original_order_id': self.id,
        }

        revised_order_id = self.copy(default=vals)
        self.state = 'has_revision'
        self._recompute_revision_count_family()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Revised Sale Order',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': revised_order_id.id,
        }

    def _get_revision_root(self):
        """Return the top-most original order"""
        self.ensure_one()
        order = self
        while order.original_order_id:
            order = order.original_order_id
        return order

    def _get_all_descendant_revisions(self):
        """Return all child revisions recursively"""
        self.ensure_one()

        def _walk(order):
            children = order.revised_order_ids
            all_children = children
            for child in children:
                all_children |= _walk(child)
            return all_children

        return _walk(self)

    def _get_full_revision_family(self):
        """
        ROOT + all revisions at all levels
        """
        self.ensure_one()
        root = self._get_revision_root()
        return root | root._get_all_descendant_revisions()

    def action_confirm(self):

        order_family = self._get_full_revision_family()

        # cancel all except the one being confirmed
        to_cancel = order_family.filtered(
            lambda o: o.id != self.id and o.state not in ['cancel']
        )

        if to_cancel:
            to_cancel.action_cancel()
        res = super().action_confirm()
        self._recompute_revision_count_family()
        return res

    def action_cancel(self):
        res = super().action_cancel()
        self._recompute_revision_count_family()
        return res

    def action_view_revised_orders(self):

        order_family = self._get_full_revision_family()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Revised Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', order_family.ids)],
            'context': {
                'create': False
            }
        }
