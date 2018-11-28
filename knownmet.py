#!/usr/bin/python3
#-*- coding: utf-8 -*-
from constant import *
from fileio import FileIO
from record import Record

class KnownMet:    
    def __init__(self, path):
        self.version = 0
        self.records = []
        with FileIO(path, "rb") as file_:
            self.__loadFromFile(file_)
            assert(len(file_.read(1)) == 0)
    
    def __loadFromFile(self, reader):
        self.version = reader.readUint8()
        if not self.version in (MET_HEADER, MET_HEADER_I64TAGS):
            raise Exception("Invailed Version 0x%02X" % (self.version,))
        record_count = reader.readUint32()
        for _ in range(0, record_count):
            record = Record()
            record.load(reader)
            self.records.append(record)

    def printDetails(self, linkOnly=False):
        if linkOnly:
            for record in self.records:
                print(record.getEd2kLink())
        else:
            from function import pformat as pf
            from function import formatSize2 as fs2
            for record in self.records:
                pf("Modification Time:", record.getFormatModifTime())
                pf("File Name:", record.getFileName())
                pf("File Size:", fs2(record.getFileSize()))
                pf("File Hash:", record.getFileHash())
                pf("AICH Hash:", record.getAichHash())
                pf("Ed2k Part Count:", record.getEd2kPartCount())
                print("-------------------------------------------------")
            pf("KnownMet Version:", "0x%02X"%(self.version,))
            pf("Record Count:", len(self.records))


def main():
    import sys
    import argparse
    
    p = argparse.ArgumentParser()
    p.add_argument("-l", dest="l", action="store_true", help="show ed2k link only")
    p.add_argument(dest="file", nargs=1, help="known.met")
    args = p.parse_args(sys.argv[1:])

    try:
        km = KnownMet(args.file[0])
        km.printDetails(args.l)
    except Exception as err:
        print("Exception:", err, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    
