#!/usr/bin/python

# You can create new tags by adding an entry to TAG_FORMATS with the regular
# expression you want to match the data on.
#
# If you want to modify the match afterwards you can create a function
# called postfilter_<tag> which takes a value as an argument and returns
# the modified value (or None to discard.)
#
# For example, you might want to convert email addresses to lowercase, in 
# which case you could do:
#
# def postfilter_email(email):
#     return email.lower()
#
# Unit tests live in tests.py, I'd recommend adding to these as you make
# changes.

from lib.domain_name import DomainName, InvalidUrlError


TAG_FORMATS = {
        'ipv4'     : (
            r'((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\d])'),

        # http://splunk-base.splunk.com/answers/8435/ipv6-addresses-parsed-properly
        'ipv6'     : (
            r'\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*'
            ),

        'url'      : r'(?:http|https)(?::\/{2}[\w]+)(?:[\/|\.]?)(?:[^\s"]*)',
        # extract as URL then convert to host/domain name
        'hostname' : r'(?:http|https)(?::\/{2}[\w]+)(?:[\/|\.]?)(?:[^\s"]*)',
        'domain'   : r'(?:http|https)(?::\/{2}[\w]+)(?:[\/|\.]?)(?:[^\s"]*)',
        
        'md5'      : r'\b[a-f\d]{32}\b',
        
        'sha1'     : r'\b[a-f\d]{40}\b',
        
        'sha256'   : r'\b[a-f\d]{64}\b',
        
        'email'    : r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}',
        }

def postfilter_hostname(url):
    """
    The 'hostname' regular expression catches an entire http URL. We use the
    DomainName class to extract the whole domain.

    >>> postfilter_hostname('http://sub1.google.com/foo/bar')
    'sub1.google.com'
    """
    try:
        d = DomainName(url)
        return d.full_domain_name()
    except InvalidUrlError:
        return None

def postfilter_domain(url):
    """
    The 'domain' regular expression catches an entire http URL. We use the
    DomainName class to extract the root domain.

    >>> postfilter_domain('http://sub1.google.com/foo/bar')
    'google.com'
    """
    try:
        d = DomainName(url)
        return d.root_domain()
    except InvalidUrlError:
        return None


