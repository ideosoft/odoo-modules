# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from datetime import date, datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning


class Salida(models.Model):

    _name="residuo.salida"
    _description="Registro Salida"
    

    def compute_total_weight(self):
        self.env.cr.execute("select sum(peso) total from residuo_entrada")
        total = self.env.cr.fetchone()[0]
        
        self.env.cr.execute("select sum(peso) recogido from residuo_entrada where recogido = 't'")
        recogido = self.env.cr.fetchone()[0]
        if not recogido:
            recogido = 0
        
        return total - recogido
        
        
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s" % (record.code or "-")))
        return result
        
    
    @api.multi
    def validate_salida(self):
        self.state = 'confirmed'
        
        
    @api.model
    def create(self, vals):
        drafts = self.env['residuo.entrada'].search([('state','=','draft'),('recogido','=',False)])
        if drafts:
            raise Warning('Tienes registros de entrada sin confirmar / imprimir.\n\nPor favor confirma todos los registros antes de continuar.')
        else:
            next_code = self.env['ir.sequence'].next_by_code('residuo.salida.seq_reg_salida')
            vals['code'] = next_code
            vals['state'] = 'draft'
            vals['total_weight'] = self.compute_total_weight()

            in_store = self.env['residuo.entrada'].search([('recogido','=',False)])
            for record in in_store:
                record.write({'recogido': True})
            
            return super(Salida, self).create(vals)
            
    
    @api.multi
    def unlink(self):
        for salida in self:
            if salida.state not in ('draft'):
                raise Warning('No se puede borrar un registro una vez que haya sido validado.')
            
        return super(Salida, self).unlink()
   
        
    code = fields.Char(string='Código', store=True, readonly=True, copy=False)
    state = fields.Selection([('draft','Borrador'),('confirmed','Confirmado')], string="Estado")
    date = fields.Date(string='Fecha Salida', default=fields.Date.today, required=True)
    total_weight = fields.Char(string="Peso total", default=compute_total_weight, store=True, readonly=True)
    notes = fields.Text(string="Observaciones")
    
