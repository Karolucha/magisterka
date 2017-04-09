# -*- coding: utf-8 -*-
import common.lxmlhelper as lxmlhelper
from datetime import datetime

import re
class HappeningWriter(object):
    def __init__(self, item_name, username="nazwa_syndykatora",path="./"):
        self.username = username
        self.path = path
        self.item=""
        self.item_name=item_name
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self,value):
        if value.endswith("/"):
            self._path = value
        else:
            self._path = "%s/"%value
    def get_modify_dt(self):
        fmt = '%Y-%m-%dT%H:%M'
        d = datetime.now()
        return d.strftime(fmt)
    def _create_xml_tree(self,happenings):
        happenings_xml=lxmlhelper.Element("happenings")
        # import_parameters=lxmlhelper.Element("import_parameters")
        # import_parameters.add_tag("user",  self.username)
        # happenings_xml.append(import_parameters)
        for single_happening in happenings:
            if single_happening and len(single_happening.keys())>1:
                try:
                    happenings_xml.append(self._create_xml_happening(single_happening))
                except Exception as e:
                    single_happening['description'] = e
                    single_happening['title'] = 'ERROR'
                    happenings_xml.append(self._create_xml_happening(single_happening))
        return happenings_xml

    def _create_xml_happening(self,item):
        happening = lxmlhelper.Element("happening")
        happening.add_tag("url",item.get("source_url"))
        happening.add_tag("title",item.get("title"))
        happening.add_tag("description",item.get("description"))
        return happening
    

           

                
    def _write_xml_to_file(self,file_name,xml_tree):
        output_file = open(file_name,"w")
        output_file.write(lxmlhelper.etree.tostring(xml_tree,pretty_print=True,encoding=str))
        output_file.close()                                    
            
      
    
    def generate_filename(self):
        file_name = self.username
        return file_name
    
    @classmethod       
    def write_to_file(cls,items, item_name,username="nazwa_syndykatora",path="./"):
        writer = cls(item_name, username,path)
        items_xml = writer._create_xml_tree(items)
        file_name = writer.generate_filename()
        # file_name = 'proba.xml'
        writer._write_xml_to_file(file_name, items_xml)             
                    
