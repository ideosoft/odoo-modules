# -*- coding: utf-8 -*-

from ftplib import FTP
import os

def ftp_list_import(self)
    ftp = FTP('ftp.xtratelecom.es')
    ftp.login('c216079', 'aPK7t42n')
    ftp.cwd("/")
    files = ftp.nlst()
    
    exits_list = []
    
    records = self.env['ideosoft.cdr.xtra.check'].search()
    for record in records:
            exits_list.append(record.name)
    
    
    for file in files:
        print file
        if not file in exits_list
            self.env['ideosoft.cdr.xtra.check'].create({'name': file})
        #ftp.retrbinary('RETR %s' % file, open(os.path.join('/tmp/', file), 'wb').write)
