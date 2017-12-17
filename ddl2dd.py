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
from collections import namedtuple

REX_MATCHER = re.compile(r"^(\w+?)\s(.+?)\s.+--dd(.+?)$")

Column = namedtuple('Column',['name','dtype','nullable','comment'])

MD_HEADER = """\n|Name|Data Type|Nullable|Comment|
|:---|:-------|:-------|:-------|"""

WIKI_HEADER = """\n||Name|||Data Type|||Nullable|||Comment||"""

class DDL(object):
    def __init__(self, table_name, ddl_text):


        self.table_name = table_name
        self.keypos = self._get_keyposes(ddl_text)

        all_lines = [x.strip() for x in ddl_text.splitlines()]

        self.table_desc = all_lines[self.keypos[0]+1: self.keypos[1]]
        column_lines = all_lines[self.keypos[2]+1: self.keypos[3]]

        self.columns = self._process_lines(column_lines)



    def __repr__(self):
        return 'DDL(table_name={})'.format(self.table_name)


    def _get_keyposes(self, ddl_text):
        """Check the input DDL, check keywords to see if valid or not

        """
        lines = [x.strip() for x in ddl_text.splitlines()]
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
        for pos, line in enumerate(lines, start=1): # easy to check all zeros
            if line == '/* desc':
                p1 = pos
            elif line == 'desc */':
                p2 = pos
            elif line == '-- ddstart':
                p3 = pos
            elif line == '-- ddend':
                p4 = pos
            else:
                pass
        if p1 == 0 or p2 == 0 or p3 == 0 or p4 == 0 \
            or p1 >= p2 or p3 >= p4:
            raise ValueError('Please check the DDL format')
        else:
            return [p-1 for p in [p1,p2,p3,p4]]

    def _process_lines(self, col_line_list):
        """Process a list of lines and output a list of `Column`
        """
        return_list = []
        for line in col_line_list:
            # remove the comma
            if line.startswith(','):
                line = line[1:].strip()

            _nullable = 'Yes'
            if not '--dd' in line:
                pass # skipped
            else:
                if 'NOT NULL' in line.upper():
                    _nullable = 'No'

                # Start REX_MATCHER
                print(line)
                reg = REX_MATCHER.match(line)
                print(reg)

                c = Column(reg.group(1).strip(),
                           reg.group(2).strip(),
                           _nullable,
                           reg.group(3).strip())
                return_list.append(c)
        return return_list

    def gen_output(self, filefmt='MD'):
        """Generate output in specific Markup language

        Markdown or Confluence Wiki
        """
        if filefmt not in ['MD','WIKI']:
            raise ValueError('Format only can be `MD` or `WIKI`')
        all_output_lines = []
        # output the table name as first line
        heading_sign = {
            'MD':'## ',
            'WIKI':'h2. '
        }

        all_output_lines.append('{prefix}{name}\n'.format(
                                                    prefix=heading_sign[filefmt]
                                                   ,name=self.table_name))
        for line in self.table_desc:
            all_output_lines.append(line.strip())


        if filefmt == 'MD':
            all_output_lines.append(MD_HEADER)
        else:
            all_output_lines.append(WIKI_HEADER)

        for c in self.columns:
            all_output_lines.append('|{}|{}|{}|{}|'.format(c.name, c.dtype,
                                                           c.nullable, c.comment))
        print('\n'.join(all_output_lines))
        return '\n'.join(all_output_lines)
