#!/usr/bin/python3
# coding: utf8

from os import path
from main import loadFile


def main():

    filePath = path.join(path.dirname(__file__), 'storage.json')
    DMs = loadFile(filePath)

    print("dumpDMs.py")
    print("===============")
    print("Dump all DMs from storage\n")

    for DM in DMs:
        print("---------------")
        DM.printDetail()

    print("---------------")
    print("You have %d DMs" % len(DMs))
    print("---------------")
    print("Done!")
    # End main()


if __name__ == '__main__':
    main()
