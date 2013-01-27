#!/usr/bin/python

"""
Parses a file to extract a tag which matches a predefined regular expression.
Example module usage:

  from extract import get_valid_tags, extract_tags, extract_tags_from_file
  print(get_valid_tags())
  extract_tags_from_file('ipv4', 'examplefile.txt')
  extract_tags('email', 'This string contains test@test.com tag data')
"""

_TAG_FORMATS = {
        'ipv4'     : (
            r'((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\d])'),
        'ipv6'     : r'',
        'url'      : r'(?:http|https)(?::\/{2}[\w]+)(?:[\/|\.]?)(?:[^\s"]*)',
        # see postfilter_hostname and postfilter_domain
        'hostname' : r'(?:http|https)(?::\/{2}[\w]+)(?:[\/|\.]?)(?:[^\s"]*)',
        'domain'   : r'(?:http|https)(?::\/{2}[\w]+)(?:[\/|\.]?)(?:[^\s"]*)',
        'md5'      : r'\b[a-f\d]{32}\b',
        'sha1'     : r'\b[a-f\d]{40}\b',
        'sha256'   : r'\b[a-f\d]{64}\b',
        'email'    : r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}',
        }

import sys
import re
import time
from lib.rfc3339 import rfc3339
from lib.domain_name import DomainName, InvalidUrlError

class UnknownTagError(Exception):
    pass


def main():
    """
    Called when invoked from the command line. Parses tag and filename and calls
    the extract_from_file function
    """
    timestamp_string = str(rfc3339(time.time()))

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
    (tag, filename) = sys.argv[1:3]

    try:
        tags = extract_from_file(tag, filename)
    except UnknownTagError, e:
        print(e)
        usage()
        sys.exit(2)
    except IOError, e:
        print(e)
        usage()
        sys.exit(3)

    for tag, matches in tags.items():
        for match in matches:
            print("tag;%s;%s;\"%s\"" % (
                timestamp_string, tag, match))

def usage():
    print("\nUsage: %s <tag> <filename>" % sys.argv[0])
    print("\nValid tags are: %s" % ','.join(get_valid_tags()))

def get_valid_tags():
    "Returns a list of strings for all supported tags."
    return _TAG_FORMATS.keys()

def extract_from_file(tag, filename):
    "Opens a file, reads its content and calls extract_tags"
    f = open(filename, 'r')
    tags = extract_tags(tag, f.read())
    f.close()
    return tags

def extract_tags(tag, text):
    """
    Searches in the string text for non-overlapping instances of the tag
    specified. Returns a dictionary of tag name to a list of matches.
    
    >>> extract_tags('ipv4', 'some text with an IP 192.168.0.1')
    {'ipv4': ['192.168.0.1']}
    """
    
    re = get_re_object(tag)
    return {tag : apply_postfilter(tag, re.findall(text))}

def apply_postfilter(tag, values):
    """
    Looks for a function called postfilter_<tag>. If found, the function is used
    to re-write the value. Used if regular expressions alone cannot do the
    extraction.
    """
    try:
        func = globals()["postfilter_%s" % tag]
        return filter(None, map(func, values))
    except KeyError:
        return values

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


def get_re_object(tag):
    "Compiles the regular expression object for the tag"
    if tag not in _TAG_FORMATS:
        raise UnknownTagError("Unknown tag '%s', valid tags are: %s" % (
            tag, ','.join(get_valid_tags())))
    return re.compile(_TAG_FORMATS[tag], re.IGNORECASE)  


if __name__ == '__main__':
    main()
