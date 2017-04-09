#-*- coding: utf-8 -*-
'''
Created on 03-12-2013

@author: michal
'''

from lxml.etree import ElementBase  
from  lxml import etree
import re
import lxml.html.clean as clean
import lxml.html as html 
def clean_html(text):
        if text is not None: 
            cleaner = clean.Cleaner(kill_tags=['a'])
            tag = html.fromstring( cleaner.clean_html(text))
            return re.sub("\s{2,}"," ",tag.text_content())
#         return "opis imprezy"


def Element(name,attrib={},**extra):
        attrib = attrib.copy()
        attrib.update(extra)
        parser_lookup = etree.ElementDefaultClassLookup(element=MyWriter)
        parser = etree.XMLParser()
        parser.set_element_class_lookup(parser_lookup)
        tag = parser.makeelement(name, attrib=attrib)
        return tag
    
def create_tag(name,value,attrib={},**extra):
#         print ("tworze tag %s o wartości %s"%(name,value))
        attrib = attrib.copy()
        attrib.update(extra)
        parser_lookup = etree.ElementDefaultClassLookup(element=MyWriter)
        parser = etree.XMLParser()
        parser.set_element_class_lookup(parser_lookup)
        tag = parser.makeelement(name, attrib=attrib) 
        if value:
#             tag.text = value.decode("utf-8")
            tag.text = value
            return tag    
    
    
class MyWriter(ElementBase):
        def add_tag(self,name,value,attr={},**extra):
            attrib = attr.copy()
            attrib.update(extra)
            if value:
                self.append(create_tag(name,value,**attrib)) 