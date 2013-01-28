#!/usr/bin/python

"""
Parses a file to extract a tag which matches a predefined regular expression,
described in tags.py

Example module usage:

  from extract import get_valid_tags, extract_tags, extract_tags_from_file
  print(get_valid_tags())
  extract_tags_from_file('ipv4', 'examplefile.txt')
  extract_tags('email', 'This string contains test@test.com tag data')
"""

import sys
import re
import time
from lib.rfc3339 import rfc3339

import tags

class UnknownTagError(Exception):
    pass

def main():
    """
    Called when invoked from the command line. Parses tag and filename and calls
    the extract_tags_from_file function
    """
    timestamp_string = str(rfc3339(time.time()))

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)
    
    (tag, filename) = sys.argv[1:3]

    try:
        tags = extract_tags_from_file(tag, filename)
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
    return tags.TAG_FORMATS.keys()

def extract_tags_from_file(tag, filename):
    "Opens a file, reads its content and calls extract_tags"
    f = open(filename, 'r')
    matching_tags = extract_tags(tag, f.read())
    f.close()
    return matching_tags

def extract_tags(tag, text):
    """
    Searches in the string text for non-overlapping instances of the tag
    specified. Returns a dictionary of tag name to a list of matches.
    
    >>> extract_tags('ipv4', 'some text with an IP 192.168.0.1')
    {'ipv4': ['192.168.0.1']}
    """
    
    re = get_re_object(tag)
    matches = map(detuple, re.findall(text))
    return {tag : apply_postfilter(tag, matches)}

def detuple(value):
    """
    Return the first value in a tuple, or the value itself if not a tuple.
    >>> detuple(('foo', 'bar'))
    'foo'
    >>> detuple('foo')
    'foo'
    """
    return value[0] if isinstance(value, tuple) else value

def apply_postfilter(tag, values):
    """
    Looks for a function called postfilter_<tag>. If found, the function is used
    to re-write the value. Used if regular expressions alone cannot do the
    extraction.
    """
    try:
        func = getattr(tags, "postfilter_%s" % tag)
        return filter(None, map(func, values))
    except AttributeError:
        return values

def get_re_object(tag):
    "Compiles the regular expression object for the tag"
    if tag not in tags.TAG_FORMATS:
        raise UnknownTagError("Unknown tag '%s', valid tags are: %s" % (
            tag, ','.join(get_valid_tags())))
    return re.compile(tags.TAG_FORMATS[tag], re.IGNORECASE)  


if __name__ == '__main__':
    main()
