# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp import api


class project_duration_timesheet(osv.osv):
    _name = "account.analytic.line"
    _inherit = "account.analytic.line"

    _columns = {
        'proj_duration_id': fields.one2many('project.duration', 'proj_duration_id')
    }

    @api.depends('unit_amount')
    def check_amount(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            pass



class project_duration_model(osv.osv):
    _inherit = "account.analytic.account"

    _columns = {
        'proj_duration_id': fields.one2many('project.duration', 'proj_duration_id')
    }

class project_duration(osv.osv):
    _name = "project.duration"
    _description = "Project duration"

    _columns = {
        'employee': fields.many2one('hr.employee', string='Employee'),
        'hours_amount': fields.float(string='Number of hours'),
        'proj_duration_id': fields.many2one('account.analytic.account', 'Model ID'),
    }
