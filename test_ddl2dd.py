# -*- coding: utf-8 -*-
import unittest
import io
from ddl2dd import DDL

class DDLTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid_ddl_true(self):
        ddl_text = """
        /* desc
        dummy
        desc */
        -- ddstart
        ,
        -- ddend
        dummy
        """
        d = DDL('filename', ddl_text)
        self.assertEqual([1,3,4,6], d.keypos)
        self.assertEqual(['dummy'], d.table_desc)

    def test_num_of_columns(self):
        ddl_text = """
        /* desc
        dummy
        desc */
        -- ddstart
        c1 varchar(11,2) not null --dd how are you
        c1 varchar(11,2) not null --dd how are you
        c1 varchar(11,2) not null --dd how are you
        -- ddend
        dummy
        """
        d = DDL('filename', ddl_text)
        self.assertEqual(3, len(d.columns))

    def test_skipped_columns(self):
        ddl_text = """
        /* desc
        dummy
        desc */
        -- ddstart
        c1 varchar(11,2) not null --dd how are you
        c1 varchar(11,2) not null
        c1 varchar(11,2) not null --dd how are you
        -- ddend
        dummy
        """
        d = DDL('filename', ddl_text)
        self.assertEqual(2, len(d.columns))

    def test_skipped_columns(self):
        ddl_text = """
        /* desc
        dummy
        desc */
        -- ddstart
        c1 varchar(11,2) not null --dd how are you
        c1 varchar(11,2) not null
        c1 varchar(11,2) not null --dd how are you
        -- ddend
        dummy
        """
        d = DDL('filename', ddl_text)
        clist = d.columns
        self.assertEqual('c1',clist[0].name)
        self.assertEqual('varchar(11,2)',clist[0].dtype)
        self.assertEqual('No',clist[0].nullable)
        self.assertEqual('how are you',clist[0].comment)

    def test_final(self):
        ddl_text = """
        /* desc
        this is table desc
        another line
        desc */
        -- ddstart
        c1 varchar(11,2) not null --dd comment1
        c2 Decimal(11,2) null --dd comment2
        -- ddend
        dummy
        """
        expect_output = """## table_name

this is table desc
another line

|Name|Data Type|Nullable|Comment|
|:---|:-------|:-------|:-------|
|c1|varchar(11,2)|No|comment1|
|c2|Decimal(11,2)|Yes|comment2|"""
        d = DDL('table_name', ddl_text)
        self.assertEqual(expect_output,d.gen_output('MD'))

    def test_final_wiki(self):
        ddl_text = """
        /* desc
        this is table desc
        another line
        desc */
        -- ddstart
        c1 varchar(11,2) not null --dd comment1
        c2 Decimal(11,2) null --dd comment2
        -- ddend
        dummy
        """
        expect_output = """h2. table_name

this is table desc
another line

||Name|||Data Type|||Nullable|||Comment||
|c1|varchar(11,2)|No|comment1|
|c2|Decimal(11,2)|Yes|comment2|"""
        d = DDL('table_name', ddl_text)
        self.assertEqual(expect_output,d.gen_output('WIKI'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DDLTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
