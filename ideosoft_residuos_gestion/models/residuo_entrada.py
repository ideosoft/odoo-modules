# -*- encoding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning
import base64

class Entrada(models.Model):

    _name="residuo.entrada"
    _description="Registro Entrada"
    
    @api.model
    def create(self, vals):
        next_number = self.pool.get('ir.sequence').get(self.env.cr, self.env.uid, 'residuo.salida.seq_reg_entrada')
        vals['number'] = next_number
        vals['state'] = 'draft'
        return super(Entrada, self).create(vals)
            
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s" % (record.number or "-")))
        return result
    
    @api.one
    @api.depends('entrada_linea_ids')
    def _compute_peso_total(self):
        total = 0
        for record in self.entrada_linea_ids:
            total += record.cantidad * record.residuo_id.peso
        self.peso = total

        
    def _get_default_company(self):
        return self.env.user.company_id
        
            
    @api.multi
    def entrada_print(self):
        self.state = 'confirmed'
        return self.env['report'].get_action(self, 'ideosoft_residuos_gestion.report_residuo')
        
        
        
    @api.multi
    def unlink(self):
        for entrada in self:
            if entrada.state not in ('draft'):
                raise Warning('No se puede borrar un registro una vez que haya sido validado / imprimido.')
            
        return super(Entrada, self).unlink()
    
    
    @api.model
    def get_companies_current_user(self):
  
        res = []
         
        self.env.cr.execute("""
                            select cu.cid, c.name, encode(p.image,'base64')
                            from res_users u, res_company_users_rel cu, res_company c, res_partner p
                            where u.id = cu.user_id
                            and cu.cid = c.id
                            and c.id = p.company_id
                            and c.partner_id = p.id
                            and u.id = %s
                            order by c.id
                            """
                            ,[self.env.user.id])

        for data in self.env.cr.fetchall():   

            if not data[2]:
                image = ''
            else: 
                image = base64.decodestring(data[2])
                
                
            res.append({
                'id': data[0],
                'name': data[1],
                'logo': image
            })

        return res
        
        
    @api.model
    def get_ids_companies_current_user(self):
        self.env.cr.execute('select cid from res_company_users_rel where user_id = %s',[self.env.user.id])
        return self.env.cr.fetchall()


        
    @api.model
    def set_user_company(self, company_id):
        if company_id:
            self.env.cr.execute("update res_users set company_id = %s where id = %s",(company_id,self.env.user.id))
            
            
    @api.model
    def hide_menu_group_gestion(self):
        action = ''
        user = self.env['res.users'].browse(self.env.user.id)
        
        for group_id in user.groups_id:
            group = self.env['res.groups'].browse(group_id.id)
            if group.full_name == 'Gestion de Residuos':
                action = 'hide'
                print group.full_name

        return action
        
        
        
    
        
    number = fields.Char(string='Number', store=True, readonly=True, copy=False)
    date = fields.Date(string="Fecha Entrada", default=fields.Date.today, required=True)
    state = fields.Selection([('draft','Borrador'),('confirmed','Confirmado')], string="Estado")
    empresa_id = fields.Many2one(comodel_name='res.company', ondelete='set null', string="Empresa", default=_get_default_company) 
    obra_id = fields.Many2one('residuo.obra', ondelete='set null', string="Obra", select=True)
    entrada_linea_ids = fields.One2many(comodel_name='residuo.entrada_linea', inverse_name='entrada_id', string="Residuos", readonly=False, copy=True)
    peso = fields.Float(string="Peso Estimado (Kg)", compute=_compute_peso_total, default=0, store=True)
    note = fields.Text("Notas")
    recogido = fields.Boolean(string="Recogido", default=False, store=True)
    
   
    
class EntradaLinea(models.Model):

    _name="residuo.entrada_linea"
    _description="Linea Entrada"
    _order = "id"
        
    @api.depends('cantidad', 'residuo.peso')
    def _compute_peso(self):
        self.peso = self.cantidad * self.residuo.peso
                
    entrada_id = fields.Many2one('residuo.entrada', string="Referencia Documento Entrada", ondelete='cascade', index=True)
    cantidad = fields.Float(string="Cantidad", required=True)
    residuo_id = fields.Many2one('residuo.tiporesiduo', string='Residuo', ondelete='set null', select=True)
