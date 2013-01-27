#!/usr/bin/python

# Copyright (c) 2012, Paul Michael Furley
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Written by: Paul Michael Furley
#    Website: paulfurley.com


"""
This library offers the DomainName class with some helper classes which aim
to make it easier to split a full domain name into its component parts:
    subdomains, root domain, effective TLD

Examples:
    
    www|google|com
    www|google|co.uk
    www|durham|ac.uk
    subdomain1.subdomain2|example|com.au

Note that this is a lightweight 'best guess' attempt. If you want real accuracy,
for example for working out how to handle cookies, please see the package
'tldextract' (https://github.com/john-kurkowski/tldextract) which uses the 
information provided at publicsuffix.org

Usage:
    from domain_name import DomainName
    d = DomainName('http://www.google.co.uk/foo/bar')
    d.root_domain()
    => 'google.co.uk'
    d.subdomains()
    => ['www']
    d.effective_tld()
    => 'co.uk'

"""

import re
import unittest


ccTLDS = [ # Country code TLDs
'ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq', 'ar', 'as',
'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi',
'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc',
'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cs', 'cu',
'cv', 'cx', 'cy', 'cz', 'dd', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee',
'eg', 'eh', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga',
'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr',
'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie',
'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke',
'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc',
'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg',
'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv',
'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np',
'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn',
'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb',
'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr',
'ss', 'st', 'su', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj',
'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug',
'uk', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws',
'ye', 'yt', 'yu', 'za', 'zm', 'zw'
]

DOMAIN_RE = re.compile(r'((?:[a-z][a-z\.\d\-]+)\.(?:[a-z][a-z\-]+))(?![\w\.])')


class InvalidUrlError(Exception):
    pass

class DomainName:
    SUBDOMAINS = 0
    ROOT = 1
    TLD = 2

    def __init__(self, fqdn):
        self.fqdn = extract_domain_name(fqdn)
        
        self.parts = None # format is ['sub1', 'sub2', 'google', 'co.uk']

    def load_parts(self):
        if self.parts is not None:
            return

        self.parts = parse_domain(self.fqdn)

    def full_domain_name(self):
        return self.fqdn

    def effective_tld(self):
        "Eg google.co.uk has an 'effective' tld of .co.uk, real tld is .uk"

        self.load_parts()
        return self.parts[DomainName.TLD]

    def root_domain(self):
        "The domain without any subdomains."
        self.load_parts()
        return '.'.join(filter(None, (
                self.parts[DomainName.ROOT],
                self.parts[DomainName.TLD])))

    def subdomains(self):
        "A list of subdomains, ie ['www', 'subdomain2']"
        self.load_parts()
        return self.parts[DomainName.SUBDOMAINS]

    def tld(self):
        "Return the real TLD, which is either generic or country code"
        self.load_parts()
        return self.parts[TLD].split('.')[-1]

def extract_domain_name(url):
    """
    >>> extract_domain_name('http://www.google.co.uk/foo/bar&x=10')
    'www.google.co.uk'
    """
    match = DOMAIN_RE.search(url, re.IGNORECASE)
    if not match:
        raise InvalidUrlError("Unable to extract a fully-qualified domain name "
                "from '%s'" % url)
    return match.group()

def parse_domain(fqdn):
    """
    Splits a fully-qualified domain name into its constituent parts: a list of
    subdomains, the base domain, then the top-level domain.

    >>> parse_domain('sub1.google.com')
    (['sub1'], 'google', 'com')
    
    >>> parse_domain('sub1.sub2.google.co.uk')
    (['sub1', 'sub2'], 'google', 'co.uk')
    """

    (subs_and_domain, tld) = split_effective_tld(fqdn)
    (subs, root) = split_subdomains_root(subs_and_domain)

    return (filter(None, subs.split('.')), 
            root, 
            tld) 

def split_effective_tld(fqdn):
    """
    >>> split_effective_tld('www.google.com')
    ('www.google', 'com')
    
    >>> split_effective_tld('www.google.co.uk')
    ('www.google', 'co.uk')
    """
    clauses = fqdn.split('.')
    if clauses[-1] in ccTLDS and clauses[-2] in ['co', 'org', 'ac', 'com']:
        tld_parts = 2
    else:
        tld_parts = 1

    root = clauses[:-tld_parts]
    effective_tld = clauses[-tld_parts:]
    return ('.'.join(root), '.'.join(effective_tld))

def split_subdomains_root(subs_and_domain):
    """
    >>> split_subdomains_root('www.google')
    ('www', 'google')
    >>> split_subdomains_root('sub1.sub2.sub3.example')
    ('sub1.sub2.sub3', 'example')
    """
    KNOWN_SUBDOMAINS = ['www', 'support']
    
    sub_parts = []
    root_parts = []

    parts = subs_and_domain.split('.')
    if parts[0] in KNOWN_SUBDOMAINS:
        return (parts[0], '.'.join(parts[1:]))
    
    return ('.'.join(parts[:-1]), parts[-1])
   

class ParseDomainTest(unittest.TestCase):
    def test_www_example_pl(self):
        self.assertEqual(
                (['www'], 'example', 'pl'),
                parse_domain('www.example.pl'))
    
    def test_example_pl(self):
        self.assertEqual(
                ([], 'example', 'pl'),
                parse_domain('example.pl'))

    def test_example_co_th(self):
        self.assertEqual(
                ([], 'example', 'co.pl'),
                parse_domain('example.co.pl'))

    def test_web_nvd_nist_gov(self):
        self.assertEqual(
                (['sub1', 'sub2'], 'site', 'gov'),
                parse_domain('sub1.sub2.site.gov'))


class DomainNameTest(unittest.TestCase):
    def setUp(self):
        self.d = DomainName('http://sub1.sub2.google.co.uk/foo/bar/')

    def test_effective_tld(self):
        self.assertEqual('co.uk', self.d.effective_tld())
    
    def test_root_domain(self):
        self.assertEqual('google.co.uk', self.d.root_domain())
    
    def test_subdomains(self):
        self.assertEqual(['sub1', 'sub2'], self.d.subdomains())

    def test_short_root_domain(self):
        d = DomainName('http://wp.me')
        self.assertEqual('wp.me', d.root_domain())

    def test_short_effective_tld(self):
        d = DomainName('http://wp.me')
        self.assertEqual('me', d.effective_tld())

    def test_bad_domain(self):
        self.assertRaises(InvalidUrlError, lambda : DomainName('http://'))



if __name__ == '__main__':
    unittest.main()
    doctest.testmod()
