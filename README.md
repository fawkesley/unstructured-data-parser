# Background

This was a piece of client work to extract various fields of information from text-based malware reports.

# Quickstart
To get started, change into the extract_tags/ directory and run the following
command:

```
$ python extract.py gauss ../examples/example3-gauss.html
```

Also have a look at import_demo.py for an indication of how to use the
extractor as a module.
Parse unstructured text to extract various bits of information

# Original Client Brief

Extract various bits of data from malware reports.
Must be an importable python library and a command-line tool.
Should not have too many dependencies.  Must be able to extract IPv4 addresses,
IPv6 addresses, hostnames & domain names (including IDNs), MD5 hashes, SHA1
hashes, SHA256 hashes, email, URL.

Must be flexible enough to allow additional data types to be parsed in the
future.

Must have a function that can be called by another python program (after
import) to extract from a variable containing the whole content of a file.

Must be useable on command-line to scan the whole content of a local file.
When called as a function or from the command-line, must have a mandatory
argument to specify the name/tag of the extraction.

The output will contain the timestamp in RFC3339 format
(1996-12-19T16:39:57-08:00) of the time when the program was invoked.

Output must in the format:
```
tag;1996-12-19T16:39:57-08:00;ipv4;"1.1.1.1"
tag;1996-12-19T16:39:57-08:00;ipv6;"fe80::200:5aee:feaa:20a2"
tag;1996-12-19T16:39:57-08:00;md5;"545cb268267609910e1312399406cdbc"
tag;1996-12-19T16:39:57-08:00;sha1;"a245efda08f2b63e0e5c1dfc0d221e3e41949194"
tag;1996-12-19T16:39:57-08:00;hostname;"calendar.google.com"
tag;1996-12-19T16:39:57-08:00;domain;"google.com"
tag;1996-12-19T16:39:57-08:00;email;"  [obscured]  "
tag;1996-12-19T16:39:57-08:00;url;"http://www.google.com";
```
etc...

Inspirations/links:
[https://github.com/stephenbrannon/IOCextractor/blob/master/IOCextractor.py](https://github.com/stephenbrannon/IOCextractor/blob/master/IOCextractor.py)
[http://tools.ietf.org/html/rfc3339](http://tools.ietf.org/html/rfc3339)

## First Iteration Feedback

With tag I meant something that can be used to store for example the name of a
project, not the data type to be extracted. Sorry if I did not make that clear.
So I would like to get extraction in one go of all the data types.

The libraries are totaly fine, but the domain library does not support IDN
(Internationalized Domain Names). Take the regexp from IOCextractor as a good
source or you can use TLDextract library -
https://github.com/john-kurkowski/tldextract

For Hostname and Domain regexp, please dont specify protocol handlers
(http/https) since there could be any or none specified.

For the Email and Url, regexp, please try to reuse the hostname regexp.

For the IPv6, please use http://forums.intermapper.com/viewtopic.php?t=452
instead which allows all the different types of IPv6 address formats that are
also listed in that post.

For hashes (MD5/sha1/sha256), please add support for mixed case hashes
(ABcDeF0128)
