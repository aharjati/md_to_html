import unittest
from md_to_html.converters.convs import HeadingConverter, LinkConverter, NoopConverter, MdProcessor
#from md_to_html.converters.processor import MdProcessor


class TestLinkConverter(unittest.TestCase):
    def test_valid_link_conversion(self):
        conv = LinkConverter(" ###     aa123 [link](http://www.link.com) as123")
        expected_html = ' ###     aa123 <a href="http://www.link.com">link</a> as123'
        self.assertEqual(conv.to_html(), expected_html)

    def test_invalid_link_conversion(self):
        conv = LinkConverter(" ###     aa123 [link] (http://www.link.com) as123")
        expected_html = ' ###     aa123 [link] (http://www.link.com) as123'
        self.assertEqual(conv.to_html(), expected_html)


class TestNoopConverter(unittest.TestCase):
    def test_valid_link_conversion(self):
        conv = NoopConverter(" ###     aa123 [link](http://www.link.com) as123")
        expected_html = '<p> ###     aa123 <a href="http://www.link.com">link</a> as123</p>'
        self.assertEqual(conv.is_valid(), True)
        self.assertEqual(conv.to_html(), expected_html)

    def test_non_link_conversion(self):
        conv = NoopConverter(" ###     aa123 as123")
        expected_html = '<p> ###     aa123 as123</p>'
        self.assertEqual(conv.is_valid(), True)
        self.assertEqual(conv.to_html(), expected_html)


class TestHeadingConverter(unittest.TestCase):

    def test_h3_conversion(self):
        conv = HeadingConverter(" ### 123")
        expected_html = "<h3>123</h3>"
        self.assertEqual(conv.is_valid(), True)
        self.assertEqual(conv.to_html(), expected_html)

    def test_h1_conversion(self):
        conv = HeadingConverter(" #    123")
        expected_html = "<h1>123</h1>"
        self.assertEqual(conv.is_valid(), True)
        self.assertEqual(conv.to_html(), expected_html)

    def test_non_lead_space_conversion(self):
        conv = HeadingConverter("#    123")
        expected_html = "<h1>123</h1>"
        self.assertEqual(conv.is_valid(), True)
        self.assertEqual(conv.to_html(), expected_html)

    def test_4_space_conversion(self):
        conv = HeadingConverter("    #    123")
        self.assertEqual(conv.is_valid(), False)
        self.assertEqual(conv.to_html(), "    #    123")

    def test_multi_space_conversion(self):
        conv = HeadingConverter("      #    123")
        self.assertEqual(conv.is_valid(), False)
        self.assertEqual(conv.to_html(), "      #    123")

    def test_3_space_conversion(self):
        conv = HeadingConverter("   #    123")
        self.assertEqual(conv.is_valid(), True)
        expected_html = "<h1>123</h1>"
        self.assertEqual(conv.to_html(),expected_html)

    def test_invalid_conversion(self):
        conv = HeadingConverter("      #123")
        self.assertEqual(conv.is_valid(), False)
        self.assertEqual(conv.to_html(), "      #123")

    def test_another_invalid_conversion(self):
        conv = HeadingConverter("      aa123")
        self.assertEqual(conv.is_valid(), False)
        self.assertEqual(conv.to_html(), "      aa123")

    def test_with_link_conversion(self):
        conv = HeadingConverter(" ###     aa123 [link](http://www.link.com) as123")
        self.assertEqual(conv.is_valid(), True)
        expected_html = '<h3>aa123 <a href="http://www.link.com">link</a> as123</h3>'
        self.assertEqual(conv.to_html(), expected_html)

    def test_with_broken_link_conversion(self):
        conv = HeadingConverter(" ### aa123 [link]( http://www.link.com ) as123")
        self.assertEqual(conv.is_valid(), True)
        expected_html = '<h3>aa123 <a href=" http://www.link.com ">link</a> as123</h3>'
        self.assertEqual(conv.to_html(), expected_html)


class TestMdProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MdProcessor()

    def test_valid_line_conversion(self):
        line = " ###     aa123 [link](http://www.link.com) as123"
        self.processor.check_append(line)
        expected_html = '<h3>aa123 <a href="http://www.link.com">link</a> as123</h3>'
        self.assertEqual(self.processor.result[0], expected_html)

    def test_invalid_line_conversion(self):
        line = "        ###     aa123 [link](http://www.link.com) as123"
        self.processor.check_append(line)
        self.assertEqual(len(self.processor.result), 0)
        self.assertEqual(self.processor.previous, "###     aa123 [link](http://www.link.com) as123\n")



if __name__ == '__main__':
    unittest.main()