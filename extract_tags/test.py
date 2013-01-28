#!/usr/bin/python

""""
Unit tests live in here to ensure that our regular expressions and postfilter
are matching correctly. These should be kept up to date as new tags are added.

To run the unit tests:
    $ python tests.py
"""

import unittest
from extract import extract_tags

class ExtractIpv4Test(unittest.TestCase):
    def do_extract(self, expected, text, tag='ipv4'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_all_zeroes(self):
        self.do_extract(['0.0.0.0'], '#0.0.0.0#')
    
    def test_multiple(self):
        self.do_extract(['0.0.0.0', '1.1.1.1'], '#0.0.0.0#1.1.1.1#')
    
    def test_all_ff(self):
        self.do_extract(['255.255.255.255'], '#255.255.255.255#')

    def test_out_of_range(self):
        self.do_extract([], '#256.256.256.256#')
   
    def test_short_formats(self):
        "Although these are valid IPs we only want to match full 4-octet IPs"
        self.do_extract([], '#192.168.1#')
        self.do_extract([], '#192.168#')
        self.do_extract([], '#192#')

class ExtractIpv6Test(unittest.TestCase):
    def do_extract(self, expected, text, tag='ipv6'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_full_address(self):
        self.maxDiff = None
        self.do_extract(
                ['fe80:0000:0000:0000:0204:61ff:fe9d:f156'], 
                '#fe80:0000:0000:0000:0204:61ff:fe9d:f156#')
    
    def test_drop_leading_zeroes(self):
        self.do_extract(
                ['fe80:0:0:0:204:61ff:fe9d:f156'], 
                '#fe80:0:0:0:204:61ff:fe9d:f156#')

    def test_collapse_multiple_zeroes(self):
        self.do_extract(
                ['fe80::204:61ff:fe9d:f156'], 
                '#fe80::204:61ff:fe9d:f156#')

    def test_ipv4_dotted_quad(self):
        self.do_extract(
                ['fe80:0000:0000:0000:0204:61ff:254.157.241.86'], 
                '#fe80:0000:0000:0000:0204:61ff:254.157.241.86#')

    def test_drop_leading_zeroes_ipv4_dotted_quad(self):
        self.do_extract(
                ['fe80:0:0:0:0204:61ff:254.157.241.86'], 
                '#fe80:0:0:0:0204:61ff:254.157.241.86#')

    def test_collapse_multiple_zeroes_ipv4_dotted_quad(self):
        self.do_extract(
                ['fe80::204:61ff:254.157.241.86'], 
                '#fe80::204:61ff:254.157.241.86#')

    def test_localhost(self):
        self.do_extract(
                ['::1'], 
                '#::1#')
    
    def test_link_local_prefix(self):
        self.do_extract(
                ['fe80::'], 
                '#fe80::#')

    def test_global_unicast_prefix(self):
        self.do_extract(
                ['2001::'], 
                '#2001::#')

class ExtractEmailTest(unittest.TestCase):
    def do_extract(self, expected, text, tag='email'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_plain_email(self):
        self.do_extract(['test@test.com'], '#test@test.com#')

class ExtractMd5Test(unittest.TestCase):
    def do_extract(self, expected, text, tag='md5'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_plain_md5(self):
        self.do_extract(
                ['0123456789abcdef0123456789abcdef'],
                '#0123456789abcdef0123456789abcdef#')

    def test_uppercase(self):
        self.do_extract(
                ['0123456789ABCDEF0123456789ABCDEF'],
                '#0123456789ABCDEF0123456789ABCDEF#')
    
    def test_invalid_letters(self):
        self.do_extract(
                [],
                '#G123456789ABCDEF0123456789ABCDEF#')

    def test_md5_no_match_inside_longer(self):
        self.do_extract(
                [],
                '#0123456789abcdef0123456789abcdef00000000#')

class ExtractUrlTest(unittest.TestCase):
    def do_extract(self, expected, text, tag='url'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_http_url(self):
        self.do_extract(['http://www.example.com'], '#http://www.example.com  ')

    def test_ftp_url(self):
        self.do_extract(['ftp://www.example.com'], '#ftp://www.example.com  ')


class ExtractBaseDomainTest(unittest.TestCase):
    def do_extract(self, expected, text, tag='domain'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_dot_com(self):
        self.do_extract(['domain.com'], 'http://sub.domain.com/foo')

    def test_dot_co_dot_uk(self):
        self.do_extract(['domain.co.uk'], 'http://sub.domain.co.uk/foo')

    def test_multi_subdomains(self):
        self.do_extract(['domain.com'], 'http://sub1.sub2.domain.com/foo')

class ExtractHostnameTest(unittest.TestCase):
    def do_extract(self, expected, text, tag='hostname'):
        self.assertEqual(
                {tag : expected},
                extract_tags(tag, text))

    def test_dot_com(self):
        self.do_extract(['sub.domain.com'], 'http://sub.domain.com/foo')

    def test_dot_co_dot_uk(self):
        self.do_extract(['sub.domain.co.uk'], 'http://sub.domain.co.uk/foo')

    def test_multi_subdomains(self):
        self.do_extract(
                ['sub1.sub2.domain.com'],
                'http://sub1.sub2.domain.com/foo')


if __name__ == '__main__':
    unittest.main()

