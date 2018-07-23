#!/usr/bin/python
import dosubby2
import os
import re
import stat
# import sys


def inner_thing(fbase):
    terminate = "\n"
    splitter = terminate + "}" + terminate
    result = []
    try:
        fp = open(fbase, "r")
        blob = fp.read(4000000)
    finally:
        fp.close

    count = 0
    uncount = 0
    chunks = blob.split(splitter)

    if len(chunks) == 1:
        terminate = "\r\n"
        splitter = terminate + "}" + terminate
        chunks = blob.split(splitter)
    if len(chunks) == 1:
        terminate = "\r"
        splitter = terminate + "}" + terminate
        chunks = blob.split(splitter)

    for chunk in chunks:
        swapped = False
        for x in range(6):
            foo = dosubby2.originala[x].search(chunk)
            if foo:
                count += 1
                result += [dosubby2.substitutea[x]]
                swapped = True
        if not swapped:
            result += [chunk]
            uncount += 1
    print('%4d\t%4d\t%4d\t%s' % (count, uncount,
                                 (len(chunks)-count-uncount), fbase))
    try:
        fp = open(fbase, "w")
        fp.write(splitter.join(result))
    finally:
        fp.close


def descend(dir):
    txt = re.compile('.*\.txt')
    for f in os.listdir(dir):
        mode = os.stat(f).st_mode
        if stat.S_ISREG(mode) and txt.search(f):
            inner_thing(f)


if __name__ == '__main__':
#    fname = sys.argv[1]
#    inner_thing("graveyard.srt.txt")
    descend(".")
