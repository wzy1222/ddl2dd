# -*- coding: utf-8 -*-
import unittest
import io
from ddl2dd import DDL

class DDLTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sample(self):
        self.assertEqual(1,1)

    def test_num_of_lines(self):
        f = io.StringIO("""1
                        --ddstart
                        2
                        3
                        --ddend
                        4""")
        ddl = DDL(f.read())
        self.assertEqual(2, len(ddl._ddl_lines))
        self.assertEqual(1, ddl.start_pos)
        self.assertEqual(4, ddl.end_pos)

    def test_full_parser(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DDLTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
