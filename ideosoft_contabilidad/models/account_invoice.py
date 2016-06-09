#-*- coding:utf-8 -*-

from openerp import models, fields, api

class account_invoice(models.Model):

    _name = 'account.invoice'
    _inherit = 'account.invoice'
    
   
    @api.one
    def cancel_validation_to_modify(self):

        # Devolvemos la factura al estado previo a la validación
        self.write({
            'state': 'draft',
        })

        invoice_id = self.ids

        moves = self.env['account.move'].search([('id','in',invoice_id)])
            
        # Cambio el estado del movimiento a borrador
        for move in moves:
            move.write({'state': 'draft'})
            
        # Cambiamos el estado de todas las líneas pertenecientes al movimiento a borrador
        lines = self.env['account.move.line'].search([('move_id','in',moves.ids)])
        for line in lines:
            line.write({'state': 'draft'})

        self.delete_workflow()
        self.create_workflow()
    
    @api.one
    def cancel_validation_to_erase(self):

        # Devolvemos la factura al estado previo a la validación
        self.write({
            'state': 'draft',
            'number': '',
            'create_date': '',
            'move_id': '',
            'internal_number': '',
            'residual': 0.00,
            'move_name': '',
            'date_invoice': None,
            'period_id': ''
        })

        invoice_id = self.ids

        moves = self.env['account.move'].search([('id','in',invoice_id)])
        
        # Cambio el estado del movimiento a borrador
        for move in moves:
            move.write({'state': 'draft'})
        
        # Cambiamos el estado de todas las líneas pertenecientes al movimiento a borrador
        lines = self.env['account.move.line'].search([('move_id','in',moves.ids)])
        for line in lines:
            line.unlink()
            
        # Cambio el estado del movimiento a borrador
        for move in moves:
            move.unlink()

        self.delete_workflow()
        self.create_workflow()