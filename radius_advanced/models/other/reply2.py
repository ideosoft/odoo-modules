class Reply(models.Model):

    _name = "radius.reply"
    _inherit = "radius.attribute"
    @api.onchange('user_id')
    
    def user_id_change(self):
        if self.user_id:
            self.username = self.user_id.username

    @api.onchange('attribute_id')
    def attribute_id_change(self):
        if self.attribute_id:
            self.attribute = self.attribute_id.attribute
            
    user_id = fields.Many2one('radius.check', string='User')
    attribute_id = fields.Many2one('radius.attribute', string='Atribute Search')  