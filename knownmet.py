#-*- coding: utf-8 -*-
from .constant import MET_HEADER, MET_HEADER_I64TAGS
from .fileio import FileIO
from .record import Record
from .function import pformat, formatSize2

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
            for record in self.records:
                pformat("Modification Time:", record.getFormatModifTime())
                pformat("File Name:", record.getFileName())
                pformat("File Size:", formatSize2(record.getFileSize()))
                pformat("File Hash:", record.getFileHash())
                pformat("AICH Hash:", record.getAichHash())
                pformat("Ed2k Part Count:", record.getEd2kPartCount())
                print("-------------------------------------------------")
            pformat("KnownMet Version:", "0x%02X"%(self.version,))
            pformat("Record Count:", len(self.records))

    @staticmethod
    def main()->int:
        import sys
        import argparse
        p = argparse.ArgumentParser()
        p.add_argument("-l", dest="l", action="store_true", help="show ed2k link only")
        p.add_argument(dest="file", nargs=1, help="known.met")
        args = p.parse_args(sys.argv[1:])
        try:
            KnownMet(args.file[0]).printDetails(args.l)
            return 0
        except Exception as err:
            print("Exception:", err, file=sys.stderr)
            return 1    

