# -*- coding: utf-8 -*-

from openerp import models, fields, api
import re
import pprint

RADIUS_ATTRIBUTE_OP = [
    ('=','='),
    (':=',':='),
    ('==','=='),
    ('+=','+='),
    ('!=','!='),
    ('>','>'),
    ('>=','>='),
    ('<','<'),
    ('<=','<='),
    ('=~','=~'),
    ('!~','!~'),
    ('=*','=*'),
    ('!*','!*'),
]

RADIUS_ATTRIBUTE_TYPE = [
    ('string','string'),
    ('integer','integer'),
    ('ipaddr','ipaddr'),
    ('date','date'),
    ('octets','octets'),
    ('ipv6addr','ipv6addr'),
    ('ifid','ifid'),
    ('abinary','abinary'),
    ('vsa','vsa'),
]

class AttributeVendor(models.Model):

    _name = "radius.attribute.vendor"
    _description = "Attribute Vendor"
        
    name = fields.Char('Name', size=64)
    
class AttributeValue(models.Model):

    _name = "radius.attribute.value"
    _description = "Attribute Value"
        
    name = fields.Char('Name', size=64)
    attribute_id = fields.Many2one(comodel_name='radius.attribute', string="Attribute", ondelete='CASCADE')
 
class Attribute(models.Model):

    _name = "radius.attribute"
    _description = "Attribute"
    _rec_name = 'display_name'
    
    @api.one
    @api.depends('attribute', 'op', 'value')
    def _compute_display_name(self):
        name = "%s" % (self.attribute)
        self.display_name = name
        
    attribute = fields.Char(string='Attribute', size=64, required=True)
    type = fields.Selection(RADIUS_ATTRIBUTE_TYPE, string='Type')
    op = fields.Selection(RADIUS_ATTRIBUTE_OP, string='OP')
    value = fields.Char('Value', size=253)
    
    active = fields.Boolean('Active', default=True)
    
    vendor_id = fields.Many2one('radius.attribute.vendor', string='Vendor')
    
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', readonly=True)
    
    value_ids = fields.One2many(comodel_name='radius.attribute.value', inverse_name='attribute_id')
    
    
class AttributeImport(models.Model):

    _name = "radius.attribute.import"
    _description = "Attribute Import"

    @api.multi
    def action_import(self):
        text = str(self.text)
        dictionary = text.split("\n")
        
        try:
            vendor_id = None
            attribute_map = {}
            for line in dictionary:
                if(re.match( r'^VENDOR', line)):
                    values = re.split( r'\s+', line)
                    vendor = values[1]
                    
                    Vendor = self.env['radius.attribute.vendor']
                    
                    vendors = Vendor.search([('name','=',vendor)])
                    
                    if vendors:
                        vendor_id = vendors._ids[0]
                    else:
                        new_obj = Vendor.create({'name': vendor})
                        vendor_id = new_obj._ids[0]

                    pprint.pprint(vendor_id)
                        
                if(re.match( r'^ATTRIBUTE', line)):
                    values = re.split( r'\s+', line)
                    attribute = values[1]
                    type = values[3]
                    if vendor_id:                    
                        vendor_id2 = self.env['radius.attribute'].create({'attribute': attribute, 'type': type, 'vendor_id': vendor_id})
                    else:
                        vendor_id2 = self.env['radius.attribute'].create({'attribute': attribute, 'type': type})
                    attribute_map[attribute] = vendor_id2
                
                if(re.match( r'^VALUE', line)):
                    values = re.split( r'\s+', line)
                    attribute = values[1]
                    name = values[2]
                    
                    print "%s %s %s" % (attribute, name, str(attribute_map[attribute].id))
                    
               
                    value_id = self.env['radius.attribute.value'].create({'name': name, 'attribute_id': attribute_map[attribute].id})
                    print value_id
                    
        except (Warning) as exc:
            raise "Error"

#            return {
#                'name': 'Hola',
#                'view_type': 'tree',
#                'view_mode': 'tree',
#                'res_model': 'radius.attribute',
#                'domain': [],
#                'context': self.env.context,
#                'type': 'ir.actions.act_window',
#                'view_id': self.env.ref("ideosoft_radius.radius_attribute_tree").id,
#            }


    text = fields.Text(string='Attribute', size=64)
    
       
