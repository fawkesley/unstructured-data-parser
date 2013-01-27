#!/usr/bin/python

"""
Program to demonstrate how to use the extract tool as an importable module.
"""

from extract_tags import extract_tags, extract_tags_from_file, get_valid_tags

def main():
    print("\nValid tags:\n    %s" % get_valid_tags())

    text = "At http://www.example.com you might see test@example.com."
    print("\nSample text:\n    %s" % text)

    matched_tags = extract_tags('email', text)
    print("\nEmails:\n    %s" % matched_tags['email'])

    matched_tags = extract_tags('hostname', text)
    print("\nHostnames:\n    %s" % matched_tags['hostname'])


if __name__ == '__main__':
    main()




