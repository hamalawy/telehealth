from DoctorLinkService_client import *
from DoctorLinkService_server import *
from DoctorLinkService_types import *

import MySQLdb
import binascii

from MHTools import get_logger

class DbLink:
# adapted from CHITS SMS project
# created by Bowei Du
    def __init__(self, *args, **kwds):
        self.dbparams = dict()
        if 'host' in kwds:
            self.dbparams['host'] = kwds['host']
        if 'port' in kwds:
            self.dbparams['port'] = int(kwds['port'])
        
        self.dbparams['user'] = kwds['user']
        self.dbparams['passwd'] = kwds['passwd']
        self.dbparams['db'] = kwds['db']
        
        log.debug('Using %s' % (str(self.dbparams)))
        #self.dbparams = {'host' : host, 'port' : port, 'user' : user, 'passwd' : passwd, 'db' : db}
        self.connect()
    
    def connect(self):
        self.conn = MySQLdb.connect(**self.dbparams)
    
    def get(self, table, cols, conds):
        if not(isinstance(cols, list) and cols):
            cols = ['*']
        if conds:
            conds_spec = []
            vals = []
            for (elem, item) in conds.items():
                conds_spec.append('%s=%%s' % elem)
                vals.append(item)
            return "SELECT %s FROM %s WHERE %s" % (','.join(cols), table, ' AND '.join(conds_spec)) , tuple(vals)
        return "SELECT %s FROM %s" % (','.join(cols), table),
    
    def insert(self, table, kv):
        cols = []
        val_spec = []
        vals = []
        for (elem, item) in kv.items():
            cols.append(elem)
            val_spec.append('%s')
            vals.append(item)
        return "INSERT INTO %s (%s) VALUES (%s);" % (table, ','.join(cols), ','.join(val_spec)), tuple(vals)
    
    def delete(self, table, conds):
        if conds:
            conds_spec = []
            vals = []
            for (elem, item) in conds.items():
                conds_spec.append('%s=%%s' % elem)
                vals.append(item)
            return "DELETE FROM %s WHERE %s" % (table, ' AND '.join(conds_spec)) , tuple(vals)
        return "DELETE FROM %s" % (table),
    
    def close(self):
        self.conn.close()
    
    def get_response(self, kw, lang):
        cur = self.conn.cursor()
        qry = self.get('responses', [lang], {'keyword': kw})
        cur.execute(*qry)
        try:
            return cur.fetchall()[0][0]
        except IndexError:
            return ''
    
    def get_earliest_msg(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT uuid from contents LIMIT 1""")
        res = cur.fetchall()
        try:
            return self.get_msg(res[0][0])
        except IndexError:
            return ()
    
    def get_msg(self, uuid):
        (contact, body) = self.get_contents(uuid)[0]
        headers = dict(self.get_headers(uuid))
        attachments = dict(self.get_attachments(uuid))
        return (contact, headers, body, attachments)
    
    def get_contents(self, uuid):
        cur = self.conn.cursor()
        qry = self.get('contents', ['contact', 'body'], {'uuid': uuid})
        cur.execute(*qry)
        return cur.fetchall()
    
    def get_headers(self, uuid):
        cur = self.conn.cursor()
        qry = self.get('headers', ['field', 'value'], {'uuid': uuid})
        cur.execute(*qry)
        return cur.fetchall()
    
    def get_attachments(self, uuid):
        cur = self.conn.cursor()
        qry = self.get('attachments', ['name', 'content'], {'uuid': uuid})
        cur.execute(*qry)
        return cur.fetchall()
    
    def set_uuid(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT UUID()""")
        # remove spatial uniqueness
        return cur.fetchall()[0][0][:23]
    
    def insert_response(self, kw, resp):
        cur = self.conn.cursor()
        #ins = self.insert('responses', {'keyword': kw})
        # add 'keyword' to dictionary
        resp.update({'keyword': kw})
        ins = self.insert('responses', resp)
        cur.execute(*ins)
        self.conn.commit()
    
    def insert_msg(self, contact, headers, body, attachments):
        uuid = self.set_uuid()
        self.insert_contents(uuid, contact, body)
        self.insert_headers(uuid, headers)
        self.insert_attachments(uuid, attachments)
        
        subj = ''
        if 'subject' in headers:
            subj = headers['subject']
        log.info("message # %s: %s" % (uuid, subj))
        
        return uuid
    
    def insert_contents(self, uuid, contact, body):
        cur = self.conn.cursor()
        ins = self.insert('contents', {'uuid': uuid, 'contact': contact, 'body': body})
        cur.execute(*ins)
        self.conn.commit()
    
    def insert_headers(self, uuid, headers):
        cur = self.conn.cursor()
        for (elem, item) in headers.items():
            ins = self.insert('headers', {'uuid': uuid, 'field': elem, 'value': item})
            cur.execute(*ins)
            self.conn.commit()
    
    def insert_attachments(self, uuid, attachments):
        cur = self.conn.cursor()
        for (elem, item) in attachments.items():
            ins = self.insert('attachments', {'uuid': uuid, 'name': elem, 'content': item})
            cur.execute(*ins)
            self.conn.commit()
    
    def del_response(self, kw):
        cur = self.conn.cursor()
        rmv = self.delete('responses', {'keyword': kw})
        cur.execute(*rmv)
        self.conn.commit()
    
    def del_msg(self, uuid):
        self.del_contents(uuid)
        self.del_headers(uuid)
        self.del_attachments(uuid)
    
    def del_contents(self, uuid):
        cur = self.conn.cursor()
        rmv = self.delete('contents', {'uuid': uuid})
        cur.execute(*rmv)
        self.conn.commit()
        
    def del_headers(self, uuid):
        cur = self.conn.cursor()
        rmv = self.delete('headers', {'uuid': uuid})
        cur.execute(*rmv)
        self.conn.commit()
    
    def del_attachments(self, uuid):
        cur = self.conn.cursor()
        rmv = self.delete('attachments', {'uuid': uuid})
        cur.execute(*rmv)
        self.conn.commit()

class WsLink:
# adapted from RxBox project
# created by Jerome Ortega
    def __init__(self):
        pass
    
    def push_msg(self, contact, headers, text_content, attachments):
        loc = DoctorLinkServiceLocator()
        port = loc.getDoctorLinkPort()
        req = push_msg()
        
        req.Contact = contact
        (req.Keys, req.Values) = self._dict_to_lists(headers)
        
        req.Text_content = text_content
        (req.File_names, req.File_contents) = self._dict_to_lists(attachments)
        resp = port.push_msg(req)
        
        return resp.Message
    
    def msg_is_sent(self, msg_sent):
        loc = DoctorLinkServiceLocator()
        port = loc.getDoctorLinkPort()
        req = msg_is_sent()
        
        req.Msg_sent = msg_sent
        
        resp = port.msg_is_sent(req)
        res = resp.Message
        
        print res
        contact = res[0]
        hnum = int(res[1])
        headers = map(self._parse_headers, res[2:hnum+2])
        text_content = res[hnum+2]
        attachments = self._generate_attachments(int(res[hnum+3]), res[hnum+4:])
        
        return (contact, dict(headers), text_content, dict(attachments))
    
    def _dict_to_lists(self, elems):
        keys = list()
        values = list()
        for (key, value) in elems.items():
            keys.append(key.lower())
            value = binascii.b2a_base64(value)
            values.append(value)
        return (keys, values)

    def _parse_headers(self, val, sep=':'):
        x = val.partition(sep)
        return (x[0].capitalize(), x[2])
    
    def _generate_attachments(self, num, elems):
        res = list()
        for index in range(0, num*2, 2):
            name = elems[index]
            cont = binascii.a2b_base64(elems[index+1])
            res.append((name, cont))
        return res

if __name__ == '__main__':
    print 'This script is not meant to be run from command line'
    log = get_logger("mhlink")
else:
    log = get_logger("mhlink")