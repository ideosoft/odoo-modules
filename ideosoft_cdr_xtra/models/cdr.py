# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date, datetime
import csv
from ftplib import FTP
import os
import csv


PATH = "/tmp/"
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
            
class TelephonyCDR(models.Model):
    
    _name = 'telephony.cdr'
    _description = "Telephony CDR"
    
    CDR_CALL_TYPES = [('DAT', 'DAT'), ('VOZ', 'VOZ'), ('SMS', 'SMS')]
        
    def init(self, cr):
        try:
            cr.execute("CREATE INDEX source_idx ON %s (source);" % self._table)
            cr.execute("CREATE INDEX destination_idx ON %s (destination);" % self._table)
            cr.execute("CREATE INDEX date_idx ON %s (date);" % self._table)
        except:
            pass
        


    @api.multi
    def _compute_human_rx(self):
        for record in self:
            record.human_rx = sizeof_fmt(record.rx)
            
    @api.multi
    def _compute_human_tx(self):
        for record in self:
            record.human_tx = sizeof_fmt(record.tx)
            
    def _search_human_tx(self, operator, value):
        return [('tx', operator, value)]
        
    def _search_human_rx(self, operator, value):
        return [('rx', operator, value)]
    
    calltype = fields.Selection(CDR_CALL_TYPES, string="Tipo")
    accountcode = fields.Char(string="Código cuenta")
    source = fields.Char(string="Origen")
    rate = fields.Char(string="Tarifa")
    destination = fields.Char(string="Destino")
    calldate = fields.Datetime(string="Fecha")
    duration = fields.Integer(string="Duración")
    tx = fields.Integer(string="tx")
    rx = fields.Integer(string="rx")  
    human_tx = fields.Char(string="HTx", compute=_compute_human_tx, search=_search_human_tx)    
    human_rx = fields.Char(string="HRx", compute=_compute_human_rx, search=_search_human_rx)
    description = fields.Char(string="Descripción")
    cost = fields.Float(string="Coste", digits=(13,8))
    
    _importdata = fields.Char(string="file:line")

    @api.one
    def insert_cdr(self):
    
        # files = [f for f in os.listdir("/tmp") if os.path.isfile(f)]
        # for f in files:
            # print(f)
    
        exists = self.env['telephony.cdr.check'].search([('name','=',filename)])
        
        #compruebo que el fichero debe ser leido para insertar datos
        if not exists or not exists.state:

            with open(PATH + filename, 'r') as f:
                reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
                
                line = 0
                for row in reader:
                    line += 1
                    if(len(row) == 12):
                    
                        date = datetime.strptime(row[5] + " " + row[6], "%d-%m-%Y %H:%M:%S")   
                    
                        new = self.env['telephony.cdr'].create({
                            'calltype': row[0],
                            'accountcode': row[1],
                            'source': row[2],
                            'rate': row[3],
                            'destination': row[4],
                            'calldate': date,
                            'duration': row[7],
                            'rx': row[8],
                            'tx': row[9],
                            'description': row[10],
                            'cost': row[11],
                            '_importdata': "%s:%d" % (filename,line)
                        })
            
            exists.write({'state':True})

            
            
            
class TelephonyCDRCheck(models.Model):

    _name = 'telephony.cdr.check'
    _description = "Telephony CDR CHECK"

    def get_ftp_conn(self):
        ftp = FTP()
        company = self.env.user.company_id
        ftp.connect(company.cdr_hostname)
        ftp.login(company.cdr_username, company.cdr_password)
        ftp.cwd("/")
        return ftp
        
        
    def truncate(self):
        table = self.env['telephony.cdr']._table
        print table
        print self.env.cr.execute("TRUNCATE TABLE %s CASCADE;" % table)
    
    
    
    @api.multi
    def read_files(self):
        
        ftp = self.get_ftp_conn()
        files_ftp = ftp.nlst()
        
        n=0
        for file in files_ftp:
            self.env['telephony.cdr.check'].create({
                'name': file,
            });
    
    
    
    @api.multi
    def import_all(self, force=False):
        
        ftp = self.get_ftp_conn()
        files_ftp = ftp.nlst()
        
        n=0
        for file in files_ftp:
            # if n < 360:
            #     n = n + 1
            #    continue
            if not os.path.exists(os.path.join('/tmp/', file)) or force:
                print "%s downloading..." % file 
                ftp.retrbinary('RETR %s' % file, open(os.path.join('/tmp/', file), 'wb').write)
            else:
                print "%s downloaded" % file
                
            with open(os.path.join('/tmp/', file), 'r') as csvf:
                reader = csv.reader(csvf, delimiter=';', quoting=csv.QUOTE_NONE)    
                line = 0
                for row in reader:
                    line += 1
                    if(len(row) == 12):
                    
                        date = datetime.strptime(row[5] + " " + row[6], "%d-%m-%Y %H:%M:%S")   
                    
                        new = self.env['telephony.cdr'].create({
                            'calltype': row[0],
                            'accountcode': row[1],
                            'source': row[2],
                            'rate': row[3],
                            'destination': row[4],
                            'calldate': date,
                            'duration': row[7],
                            'rx': row[8],
                            'tx': row[9],
                            'description': row[10],
                            'cost': row[11],
                            '_importdata': "%s:%d" % (file,line)
                        })
                        
                        # print new.id
                        
    @api.multi
    def ftp_import_cdr(self):
        ftp = selfget_ftp_conn()
        files_ftp = ftp.nlst()
        
        files_request = []
        
        for record in self:
            files_request.append(record.name)
            
        files_to_import = list(set(files_ftp) & set(files_request))
        
        if file in files_to_import:
            ftp.retrbinary('RETR %s' % file, open(os.path.join('/tmp/', file), 'wb').write)
            print file 
                
    @api.one
    def x_import(self):
        print self.name
        
    @api.one
    def ftp_list_import(self):
        ftp = self.get_ftp_conn()
        
        exits_list = []
        
        records = self.env['telephony.cdr.check'].search([])
        for record in records:
            exits_list.append(record.name)
        
        for file in files:
            print file
            if not file in exits_list:
                self.env['telephony.cdr.check'].create({'name': file})

                
    @api.one
    def compute_download(self):
        self.download = os.path.exists(os.path.join('/tmp/', self.name))
                
    name = fields.Char(string="Fichero")
    state = fields.Boolean(string="Estado", default=False)
    download = fields.Boolean(compute=compute_download, readonly=True)
    
    