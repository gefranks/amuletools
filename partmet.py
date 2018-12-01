#!/usr/bin/python3
#-*- coding: utf-8 -*-
from constant import *
from record import Record
from fileio import FileIO
from function import pformat, formatSize2

class PartMet:
    def __init__(self, path):
        self.version = 0
        self.record = Record()
        with FileIO(path, "rb") as file_:
            self.__loadFromFile(file_)
            assert(len(file_.read(1)) == 0)
        
    def __loadFromFile(self, reader):
        start_pos = reader.tell()
        self.version = reader.readUint8()
        if not self.version in (PARTFILE_VERSION,
                                PARTFILE_SPLITTEDVERSION,
                                PARTFILE_VERSION_LARGEFILE):
            raise Exception("Invailed Version 0x%02X"%(self.version,))
        
        isnewstyle = PARTFILE_SPLITTEDVERSION == self.version
        partmettype = PMT_DEFAULTOLD

        if isnewstyle:
            partmettype = PMT_SPLITTED
        else:
            reader.seek(start_pos+24)
            if reader.readUint32() == 0x01020000:
                #edonkeys so called "old part style"
                isnewstyle, partmettype = (True, PMT_NEWOLD)
            reader.seek(start_pos+1)

        if isnewstyle:
            if reader.readUint32() == 0: #0.48 partmets - different again
                self.record.loadHashs(reader)
            else:
                reader.seek(start_pos+2)
                self.record.loadModifTime(reader)
                self.record.loadHashs(reader, loadFileHashOnly=True)
        else:
            self.record.loadModifTime(reader)
            self.record.loadHashs(reader)

        self.record.loadTags(reader, isnewstyle, partmettype)

    def printDetails(self, hashsOnly=False, areaOnly=False, linkOnly=False):
        if hashsOnly:
            for h in self.record.head[Record.PartHashs]:
                print(h.hex().upper())
            return
        if areaOnly:
            for area in self.record.arealist:
                print(area.start, area.end)
            return
        if linkOnly:
            print(self.record.getEd2kLink())
            return

        pformat("PartMet Version:", "0x%02X"%(self.version,))
        pformat("Modification Time:", self.record.getFormatModifTime())
        pformat("Last Seen Complete:", self.record.getFormatLastSeenComplete())
        pformat("File Name:", self.record.getFileName())
        pformat("Part Name:", self.record.getPartName())
        pformat("File Size:", formatSize2(self.record.getFileSize()))
        pformat("File Hash:", self.record.getFileHash())
        pformat("AICH Hash:", self.record.getAichHash())
        pformat("Part Hash Count:", self.record.getEd2kPartCount())
        pformat("Progress:", self.record.getFormatProgress())


def main():
    import sys
    import argparse
    
    p = argparse.ArgumentParser()
    p.add_argument("-p", dest="p", action="store_true", help="show part hashs only")
    p.add_argument("-a", dest="a", action="store_true", help="show incomplete area only")
    p.add_argument("-l", dest="l", action="store_true", help="show ed2k link only")
    p.add_argument(dest="files", nargs="+", help="XXX.part.met")
    args = p.parse_args(sys.argv[1:])

    try:
        for path in args.files:
            pm = PartMet(path)
            pm.printDetails(args.p, args.a, args.l)    
    except Exception as err:
        print("Exception:", err, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
