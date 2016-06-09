# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, addons
import openerp

#Fix base_iban module
del addons.base_iban.base_iban.res_partner_bank._constraints
del addons.base_iban.base_iban.res_partner_bank.create

def modulo(cifras, divisor):
    """
    El entero más grande en Python es 9.223.372.036.854.775.807 (2**63-1)
    que tiene 19 cifras, de las cuales las 18 últimas pueden tomar cualquier valor.
    El divisor y el resto tendrán 2 cifras. Por lo tanto CUENTA como tope
    puede ser de 16 cifras (18-2) y como mínimo de 1 cifra.
    """
    CUENTA, resto, i = 13, 0, 0
    while i < len(cifras):
        dividendo = str(resto) + cifras[i: i+CUENTA]
        resto = int(dividendo) % divisor
        i += CUENTA
    return resto
    
def valorCifras(cifras):
    LETRAS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" # A=10, B=11, ... Z=35
    items = []
    for cifra in cifras:
        posicion = LETRAS.find(cifra)
        items.append(str(posicion) if posicion >= 0 else "-")
    return "".join(items)
    
def calcularIBAN(ccc, pais="es"):
    pais = pais.upper()
    cifras = ccc + valorCifras(pais) + "00"
    resto = modulo(cifras, 97)
    return pais + str(98 - resto).zfill(2) + ccc
    

def _format_acc(iban_str):
    res = ""
    if iban_str:
        for char in iban_str:
            if char.isalnum():
                res += char.upper()
    return res

def _pretty_iban(iban_str):
    "return iban_str in groups of four characters separated by a single space"
    res = []
    while iban_str:
        res.append(iban_str[:4])
        iban_str = iban_str[4:]
    return ' '.join(res)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    
    @api.model
    def create(self, values, context=None):
        return super(ResPartnerBank, self).create(values)
            
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Bank country',
        change_default=False,
        default=lambda self: self.env.user.company_id.country_id
    )
        
    @api.multi
    def bank_to_iban(self):
        for bank in self:
            if bank.state == 'bank':
                bank.acc_number = calcularIBAN(_format_acc(bank.acc_number))
                bank.state = 'iban'
                
                if not bank.bank:
                    bank.acc_number_change()
                    bank.bank_change()
        
    @api.onchange('bank')
    def bank_change(self):
        if self.bank:
            self.bank_name = self.bank.name
            self.bank_bic = self.bank.bic
        
        
    @api.onchange('acc_number')
    def acc_number_change(self):
        if self.acc_number:
            iban = _format_acc(self.acc_number)
            
            if len(iban) > 8:
                bank_code = iban[4:8]
                
                result = self.env['res.bank'].search([('code','=',bank_code)])
                if result:
                    self.bank = result
                
                self.acc_number = iban

    def check_iban(self, cr, uid, ids, context=None):
        return True
        
    _constraints = []