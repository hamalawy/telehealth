#!/usr/bin/python

import unittest
import xml.dom.minidom as minidom

import os.path
import ConfigParser
import cPickle
import email

from MHTools import project_path
from MHTools import XmlWrapper
from MHLink import DbLink, WsLink

class DbLinkTest(unittest.TestCase):
    """DbLink tests."""
    
    def setUp(self):
        self.xml = XmlWrapper(minidom.parse(os.path.join(PATH, 'test', "mhlink.test")))
        tags = self.xml.test.database.children()
        
        db_params = {}
        for elem in tags:
            elem_name = str(elem.__str__().strip())
            if not elem_name:
                continue
            db_params[elem_name] = str(elem.get_text())
        
        self.reader = DbLink(**db_params)
    
    def tearDown(self):
        self.reader.close()
    
    def test_set_uuid(self):
        """set_uuid() should return a string containing uuid (without spatial uniqueness)"""
        uuid = self.reader.set_uuid()
        print uuid
        self.assertTrue(isinstance(uuid, str))
    
    def test_get(self, table, cols, conds):
        pass
    
    def insert(self, table, kv):
        pass
    
    def delete(self, table, conds):
        pass
    
    def get_response(self, kw, lang):
        pass
    
    def get_earliest_msg(self):
        pass
    
    def get_msg(self, uuid):
        pass
    
    def get_contents(self, uuid):
        pass
    
    def get_headers(self, uuid):
        pass
    
    def get_attachments(self, uuid):
        pass
    
    def set_uuid(self):
        pass
    
    def insert_response(self, kw, resp):
        pass
    
    def insert_msg(self, contact, headers, body, attachments):
        pass
    
    def insert_contents(self, uuid, contact, body):
        pass
    
    def insert_headers(self, uuid, headers):
        pass
    
    def insert_attachments(self, uuid, attachments):
        pass
    
    def del_response(self, kw):
        pass
    
    def del_msg(self, uuid):
        pass
    
    def del_contents(self, uuid):
        pass
        
    def del_headers(self, uuid):
        pass
    
    def del_attachments(self, uuid):
        pass

if __name__ == "__main__":
    PATH = project_path()
    unittest.main()
