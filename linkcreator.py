#!/bin/env python3
#-*- coding: utf-8 -*-

# PartHashs:
#   FileSize(1        ) --> PartCount(1): [md4(1)      ]
#   FileSize(9728000  ) --> PartCount(2): [md4(9728000)][md4(0)      ]
#   FileSize(9728000+1) --> PartCount(2): [md4(9728000)][md4(1)      ]

# FileHash:
#   PartCount == 1: FileHash = PartHashs[0]
#   PartCount  > 1: FileHash = md4(PartHashs[...])
#   PartCount == 0: assert(False)

import hashlib

class LinkCreator:    
    def __init__(self, path):
        import os.path
        self.name_ = os.path.basename(path).strip().replace(" ", "_")
        self.size_ = os.path.getsize(path)
        if len(self.name_) == 0 or self.size_ == 0:
            raise ValueError("Invalid Argument")
        self.hash_ = bytes()
        self.hashs = []
        with open(path, "rb") as file_:
            self.__createFromFile(file_)
            assert(len(file_.read(1)) == 0)

    def __createPartHash(self, binfile, len_):
        md4 = hashlib.new("md4")
        while len_ > 0:
            d = binfile.read(min(8192, len_))
            md4.update(d)
            len_ -= len(d)
        return md4.digest()
        
    def __createFromFile(self, binfile):
        PS = 9728000
        sz = self.size_
        while sz >= PS:
            self.hashs.append(self.__createPartHash(binfile, PS))
            sz -= PS

        assert(0 <= sz < PS)
        self.hashs.append(self.__createPartHash(binfile, sz))

        if len(self.hashs) > 1:
            md4 = hashlib.new("md4")
            for h in self.hashs: md4.update(h)
            self.hash_ = md4.digest()
        else:
            self.hash_ = self.hashs[0]

    def getEd2kLink(self, hasPartHash=False):
        link = "ed2k://|file|%s|%s|%s" % (self.name_, self.size_,
                                          self.hash_.hex().upper())
        if hasPartHash and len(self.hashs) > 1:
             link += "|p=" + self.hashs[0].hex().upper()
             for h in self.hashs[1:]:
                 link += ":" + h.hex().upper()
        link += "|/"
        return link

    @staticmethod
    def main()->int:
        import sys
        import argparse
        p = argparse.ArgumentParser()
        p.add_argument("-p", dest="p", action="store_true", help="append part hashs")
        p.add_argument(dest="files", nargs="+", help="files")
        args = p.parse_args(sys.argv[1:])
        try:
            for path in args.files:
                l = LinkCreator(path)
                print(l.getEd2kLink(args.p))
            return 0
        except Exception as err:
            print("Exception:", err, file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(LinkCreator.main())
