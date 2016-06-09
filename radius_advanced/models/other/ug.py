    user_id = fields.Many2one('radius.check', string='Username')
    group_id = fields.Many2one('radius.group', string='Group')

    username = fields.Char('Username', related='user_id.username', store=True)
    groupname = fields.Char('Groupname', related='group_id.groupname', store=True) 