    @api.onchange('attribute_id')
    def attribute_id_change(self):
        if self.attribute_id:
            self.attribute = self.attribute_id.attribute
            
    group_id = fields.Many2one('radius.group', string='Group')
    attribute_id = fields.Many2one('radius.attribute', string='Atribute Search')