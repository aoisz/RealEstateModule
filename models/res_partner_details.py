from odoo import fields, models, api
import logging
import json

_logger = logging.getLogger(__name__)

class FriendPartnerDetails(models.Model):
    _inherit = "res.partner"

    friend_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="friend_partner_rel",
        column1="parent_partner_id",
        column2="child_partner_id",
        string="Friend",
        ondelete="cascade"
    )

    co_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="co_partner_rel",
        column1="parent_partner_id",
        column2="child_partner_id",
        string="Co-Partner",
        domain="[('id', 'in', friend_partner_ids)]",
        ondelete="cascade"
    )

    team_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="team_partner_rel",
        column1="parent_partner_id",
        column2="child_partner_id",
        string="Team",
        ondelete="cascade",
        domain="[('id', 'in', co_partner_ids)]",
    )

    friend_domain = fields.Char(
        readonly=True,
        compute="_visible_domain",
    )

    def friend_visible_domain(self):
        for record in self:
            visible_partner = []
            if not record.friend_partner_ids["id"]:
                record.friend_domain = "[]"
            for contact in record.friend_partner_ids:
                visible_partner.append(contact["id"])
            record.friend_domain = json.dumps(
                [('id', '!=', record.contact_id["id"]), ('id', 'in', visible_partner)]
            )

    def get_partner_domain(self,type):
        user = self.env['res.users'].sudo().search(
            [('id','=',self.env.user.id)]
        )
        partner_ids = []
        partner_list = []
        if type == "friend":
            partner_list = user.friend_partner_ids
        elif type == "co_partner":
            partner_list = user.co_partner_ids
        elif type == "team":
            partner_list = user.team_partner_ids

        for partner in partner_list:
            partner_ids.append(partner["id"])
            
        domain = [('id','in',partner_ids)]
        return domain

    @api.model
    def show_friend_list(self):
        context = {}
        view_kanban_id = self.env.ref('base.res_partner_kanban_view').id
        view_tree_id = self.env.ref('base.view_partner_tree').id
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
        }
        action.update({
            'name': 'Bạn Bè',
            'view_mode': 'kanban,tree',
            'views': [[view_kanban_id, 'kanban'], [view_tree_id, 'tree']],
            'domain': self.get_partner_domain("friend"),
            'context': context
        })
        return action

    @api.model    
    def show_co_partner_list(self):
        context = {}
        view_kanban_id = self.env.ref('base.res_partner_kanban_view').id
        view_tree_id = self.env.ref('base.view_partner_tree').id
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
        }
        action.update({
            'name': 'Đối Tác',
            'view_mode': 'kanban,tree',
            'views': [[view_kanban_id, 'kanban'], [view_tree_id, 'tree']],
            'domain': self.get_partner_domain("co_partner"),
            'context': context
        })
        return action

    @api.model    
    def show_team_list(self):
        context = {}
        view_kanban_id = self.env.ref('base.res_partner_kanban_view').id
        view_tree_id = self.env.ref('base.view_partner_tree').id
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
        }
        action.update({
            'name': 'Công Ty',
            'view_mode': 'kanban,tree',
            'views': [[view_kanban_id, 'kanban'], [view_tree_id, 'tree']],
            'domain': self.get_partner_domain("team"),
            'context': context
        })
        return action
        