# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Acct(models.Model):
    
    _name = 'radius.acct'
    _description = "Acct"
    _table = 'radacct'
    
    def init(self, cr):
        cr.execute("""
GRANT SELECT ON radcheck TO radius;
GRANT SELECT ON radreply TO radius;
GRANT SELECT ON radgroupcheck TO radius;
GRANT SELECT ON radgroupreply TO radius;
GRANT SELECT ON radusergroup TO radius;
GRANT SELECT, INSERT, UPDATE ON radippool TO radius;
GRANT SELECT, USAGE ON radippool_id_seq TO radius; 
GRANT SELECT, INSERT, UPDATE ON radacct TO radius;
GRANT SELECT, USAGE ON radacct_id_seq TO radius; 
""")
        
        
    acctsessionid = fields.Char()
    acctuniqueid = fields.Char()
    
    username = fields.Char()
    groupname = fields.Char()
    realm = fields.Char()
    nasipaddress = fields.Char()
    nasportid = fields.Char()
    nasporttype = fields.Char()
    
    acctstarttime = fields.Datetime(default=None)
    acctupdatetime = fields.Datetime(default=None)
    acctstoptime = fields.Datetime(default=None)
    
    acctinterval = fields.Integer()
    acctsessiontime = fields.Integer()
    acctauthentic = fields.Char()
    
    connectinfo_start = fields.Char()
    connectinfo_stop = fields.Char()
    acctinputoctets = fields.Float(string="Input Octets")
    acctoutputoctets = fields.Float(string="Output Octets")
    calledstationid = fields.Char()
    callingstationid = fields.Char()
    acctterminatecause = fields.Char()
    servicetype = fields.Char()
    framedprotocol = fields.Char()
    framedipaddress = fields.Char()
    
    
"""
CREATE TABLE radacct (
	RadAcctId		bigserial PRIMARY KEY,
	AcctSessionId		text NOT NULL,
	AcctUniqueId		text NOT NULL UNIQUE,
	UserName		text,
	GroupName		text,
	Realm			text,
	NASIPAddress		inet NOT NULL,
	NASPortId		text,
	NASPortType		text,
	AcctStartTime		timestamp with time zone,
	AcctUpdateTime		timestamp with time zone,
	AcctStopTime		timestamp with time zone,
	AcctInterval		bigint,
	AcctSessionTime		bigint,
	AcctAuthentic		text,
	ConnectInfo_start	text,
	ConnectInfo_stop	text,
	AcctInputOctets		bigint,
	AcctOutputOctets	bigint,
	CalledStationId		text,
	CallingStationId	text,
	AcctTerminateCause	text,
	ServiceType		text,
	FramedProtocol		text,
	FramedIPAddress		inet
);
"""