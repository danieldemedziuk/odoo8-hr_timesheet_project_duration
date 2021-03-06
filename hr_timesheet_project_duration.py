# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class project_duration_timesheet(osv.osv):
    _inherit = "hr_timesheet_sheet.sheet"

    _columns = {
        'projects_list': fields.many2one('account.analytic.account', 'Projects List'),
        'timesheet_line': fields.many2one('hr.analytic.timesheet', 'Timesheet line'),
        'project_duration_ids': fields.many2one('project.duration', 'Project duration')
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(project_duration_timesheet, self).write(cr, uid, ids, vals, context=context)
        number = 0.0

        for rec in self.browse(cr, uid, ids, context=context):
            print "CURR", rec.search_read([('user_id', '=', uid)])

            for num in range(len(rec.timesheet_ids)):
                number += rec.timesheet_ids[num]['unit_amount']
                print "PROJECT", rec.timesheet_ids[num]['account_id']['name']
            print "UNIT", number

            proj_name = rec.timesheet_ids[num]['account_id']['name']
            emp_name = rec.timesheet_ids[num]['user_id']['name']
            project_id = rec.projects_list.search([('name', '=', proj_name)])
            proj_duration_id = rec.project_duration_ids.search(['&', ('employee.user_id', '=', uid), ('proj_duration_id', '=', proj_name)])
            proj_duration_hours = proj_duration_id['hours_amount']
            proj_duration_employee = proj_duration_id['employee']['name']

            # print "PRO", rec.projects_list.search(["|", ('user_id', '=', uid), ('name', '=', rec.timesheet_ids[num]['unit_amount'])])
            # print proj_duration_employee, proj_duration_hours
            # print "emp_name", emp_name
        if (emp_name == proj_duration_employee) and (number <= proj_duration_hours):

            return res

        else:
            raise osv.except_osv(('Warning!'),
                                 ('You are not on the list of employees assigned to the project or your number of hours per project is exhausted. Check the correctness of the project and number of hours or contact the administrator.'))


class project_duration_model(osv.Model):
    _inherit = "account.analytic.account"

    _columns = {
        'project_duration_ids': fields.one2many('project.duration', 'proj_duration_id')
    }

class project_duration(osv.Model):
    _name = "project.duration"
    _description = "Project duration"

    _columns = {
        'employee': fields.many2one('hr.employee', string='Employee', store=True),
        'hours_amount': fields.float(string='Number of hours', store=True),
        'proj_duration_id': fields.many2one('account.analytic.account', 'Model ID'),
    }