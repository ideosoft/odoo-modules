# -*- encoding: utf-8 -*-

import logging
from StringIO import StringIO
import time

from openerp import api, fields, models, sql_db, SUPERUSER_ID, tools
from openerp.exceptions import Warning
from openerp.modules.registry import Registry
from openerp.osv import osv, orm
from openerp.tools import convert_xml_import
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

def _get_exception_message(exception):
    msg = isinstance(exception, (osv.except_osv, orm.except_orm)) and exception.value or exception
    return tools.ustr(msg)


SCRIPT_TYPES = [
    ('python', 'Python'),
    ('sql', 'SQL'),
    ('xml', 'XML')
]

class Script(models.Model):
    _name = 'res.script'
    _description = 'Script'

    name = fields.Char(size=128, required=True, readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Text(required=False, readonly=True, states={'draft': [('readonly', False)]})
    type = fields.Selection(SCRIPT_TYPES, 'Type', required=True)
    
    code = fields.Text(string="Code")
    state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated')], required=True, readonly=True, default='draft')
    
    automatic_dump = fields.Boolean('Automatic dump', help='Make sure postgresql authentification is correctly set', default=True)
    expect_result = fields.Boolean('Expect a result')
    
    console = fields.Text(string="Code")

    @staticmethod
    def run_script(script,args=[]):
        print "exec %s(%s)" % (script, args)
        pass

    @api.multi
    def write(self, vals):
        if not vals:
            return True
        return super(Script, self).write(vals)

    @api.multi
    def unlink(self):
        return super(Script, self).unlink()

    def copy_data(self, cr, uid, script_id, default=None, context=None):
        default = default.copy() if default else {}
        return super(Script, self).copy_data(cr, uid, script_id, default, context)


    def run_script(self, cr, uid, name):
        self.pool['res.script'].browse(cr, uid,[1]).run()
        
    @api.one
    def _run(self):
        if self.type == 'sql':
            return self._run_sql()
        elif self.type == 'xml':
            return self._run_xml()
        elif self.type == 'python':
            return self._run_python()
        raise NotImplementedError(self.type)

    @api.one
    def run(self):
        cr, uid, context = self.env.args

        if not context.get('do_not_use_new_cursor'):
            intervention_cr = sql_db.db_connect(cr.dbname).cursor()
        else:
            intervention_cr = cr
        intervention_vals = {}
        try:
            _logger.info('Running script: %s\nCode:\n%s' % (self.name.encode('utf-8'), self.code.encode('utf-8')))
            result = self.with_env(self.env(cr=intervention_cr))._run()
            self.console = result[0][0]
            if not context.get('do_not_use_new_cursor') and context.get('test_mode'):
                _logger.info('TEST MODE: Script rollbacking')
                intervention_cr.rollback()
            elif not context.get('do_not_use_new_cursor'):
                intervention_cr.commit()
            _logger.info('Script execution SUCCEEDED: %s\n' % (self.name.encode('utf-8'),))
        except Exception, e:
            _logger.error('Script execution FAILED: %s\nError:\n%s' % (self.name.encode('utf-8'), _get_exception_message(e).encode('utf-8')))
            import sys,traceback
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            
        finally:
            if not context.get('do_not_use_new_cursor'):
                intervention_cr.close()
        # intervention_vals.update({'end_date': time.strftime('%Y-%m-%d %H:%M:%S')})
        # return intervention.write(intervention_vals)
        return

    @api.one
    def _run_python(self):
        from cStringIO import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

    
        localdict = {
            'sys.stdout': mystdout,
            'self': self,
            'pool': self.pool,
            'cr': self._cr,
            'uid': self._uid,
            'context': self._context,
            'ref': self.env.ref,
            'logger': False,
            'time': time,
            'netsvc': False,
            'tools': tools,
            'SUPERUSER_ID': SUPERUSER_ID,
            'ustr': tools.ustr,
        }
        exec self.code in localdict
        #return localdict['result'] if 'result' in localdict else 'No expected result'
        sys.stdout = old_stdout
        r = mystdout.getvalue()
        mystdout.close()
        return r
        
        
    @api.one
    def _run_sql(self):
        self._cr.execute(self.code)
        if self.expect_result:
            return tools.ustr(self._cr.fetchall())
        return 'No expected result'

    @api.one
    def _run_xml(self):
        convert_xml_import(self._cr, __package__, StringIO(self.code.encode('utf-8')))
        return 'No expected result'
