# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from datetime import date


class PartnerStudies(models.Model):
    _name = 'hc.studies'
    _description = 'Partner Studies'

    name = fields.Char()


class PartnerPermit(models.Model):
    _name = 'hc.permit'
    _description = 'Partner Permits'

    name = fields.Char()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(
        string='Age',
        required=False,
        compute='_compute_age')
    citizenship_id = fields.Many2one(
        comodel_name='res.country',
        string='Citizenship',
        ondelete='restrict')
    residence = fields.Selection(
        string='Residence',
        selection=[('main', 'Main Residence'),
                   ('secondary', 'Secondary Residence')],
        required=False)
    first_lease_start = fields.Date(
        string='First Lease Start',
        required=False,
        compute='_compute_lease_dates')
    current_lease_start = fields.Date(
        string='Current Lease Start',
        required=False,
        compute='_compute_lease_dates')
    lease_end = fields.Date(
        string='Lease End',
        compute='_compute_lease_dates',
        store=True)
    current_lease_id = fields.One2many(
        comodel_name='hc.lease',
        compute='_compute_lease_dates',
    )
    lease_ids = fields.One2many(
        comodel_name='hc.lease',
        inverse_name='tenant_id',
        string='Leases')

    attachment_number = fields.Integer(
        compute='_get_attachment_number',
        string="Number of Attachments")
    attachment_ids = fields.One2many(
        comodel_name='ir.attachment',
        inverse_name='res_id',
        string='Attachments',
        domain=[('res_model', '=', 'res.partner')],
    )

    @api.multi
    @api.depends('lease_ids', 'lease_ids.start', 'lease_ids.end', 'lease_ids.state')
    def _compute_lease_dates(self):
        for partner in self:
            leases = partner.lease_ids
            partner.first_lease_start = leases.sorted(lambda l: l.start).start
            current_lease = leases.filtered(lambda l: l.state == 'ongoing')
            partner.current_lease_id = current_lease
            partner.current_lease_start = current_lease.start
            partner.lease_end = current_lease.end

    @api.multi
    @api.depends('birthdate_date')
    def _compute_age(self):
        today = date.today()
        for partner in self:
            if partner.birthdate_date:
                bd = partner.birthdate_date
                partner.age = (
                        today.year - bd.year -
                        ((today.month, today.day) < (bd.month, bd.day))
                )
            else:
                partner.age = False

    @api.multi
    def _get_attachment_number(self):
        read_group_res = (
            self.env['ir.attachment']
                .read_group([('res_model', '=', 'res.partner'),
                             ('res_id', 'in', self.ids)],
                            ['res_id'],
                            ['res_id'])
        )
        attach_data = dict(
            (res['res_id'], res['res_id_count']) for res in read_group_res
        )
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        return action

    @api.multi
    def action_set_address_from_lease(self):
        for partner in self:
            lease = partner.current_lease_id
            if lease:
                building = lease.housing_id.building_id
                if partner.residence == 'secondary':
                    partner.has_secondary_address = True
                    partner.street_secondary = building.street
                    partner.street_number_secondary = building.street_number
                    partner.zip_code_secondary = building.zip_code
                    partner.state_id_secondary = building.state_id
                    partner.country_id_secondary = building.country_id
                else:
                    partner.street = building.street
                    partner.street_number = building.street_number
                    partner.zip_code = building.zip_code
                    partner.state_id = building.state_id
                    partner.country_id = building.country_id
