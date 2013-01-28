#!/usr/bin/python

"""
Program to demonstrate how to use the extract tool as an importable module.
"""

from extract_tags import (extract_tags, get_valid_tags, create_string_output)

def main():
    print("\nValid tags:\n    %s" % get_valid_tags())

    text = "At http://www.example.com you might see test@example.com."
    print("\nSample text:\n    %s" % text)

    matched_tags = extract_tags(text)
    print("\nMatching tags:\n    %s" % matched_tags)

    print("\nMatching tags as string report:\n\n%s" % create_string_output(matched_tags, 'demo'))


if __name__ == '__main__':
    main()




