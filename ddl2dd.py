# -*- coding: utf-8 -*-
"""
Load a Teradata DDL file, and output Data Dictionary
DDL:
    AT_Product_L1_Desc VARCHAR(200) NOT NULL, --dd The comment 1
    AT_Product_L2_Desc VARCHAR(200) NOT NULL, --dd The comment 2
    AT_Product_L3_Desc VARCHAR(200) NOT NULL,
"""
import os.path
import re


class DDL(object):
    def __init__(self, ddl_text, start='--ddstart', end='--ddend', comm_sep='--dd'):
        if not ddl_text:
            raise ValueError('Please provide the ddl as text')
        self.ddl_text = ddl_text
        self._comm_sep = comm_sep

        file_lines = [x.strip() for x in ddl_text.splitlines()]
        for pos, line in enumerate(file_lines):
            if line == start:
                self.start_pos = pos
            elif line == end:
                self.end_pos = pos
            else:
                pass
        self._ddl_lines = file_lines[self.start_pos+1: self.end_pos]


    def __repr__(self):
        return 'DDL(ddl_text={})'.format(self.ddl_text[:10])

    def gen_output(filefmt='MD'):
        """Generate output in specific Markup language

        Markdown or Confluence Wiki
        """
        pass
