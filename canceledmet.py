#-*- coding: utf-8 -*-
from .fileio import FileIO
from .record import Record
from .function import pformat

class CanceledMetException(Exception):
    pass

class CanceledMet:
    AMULE_VERSION = 0x21
    VERSION = 0x0F
    OLD_VERSION = 0x0E
    
    def __init__(self, path):
        self.cancelledFilesSeed = 0
        self.version = 0
        self.hashs = set()
        with FileIO(path, "rb") as file_:
            self.__load(file_)
            assert(len(file_.read(1)) == 0)

    def __load(self, reader):
        self.version = reader.readUint8()
        if self.version == CanceledMet.VERSION:
            if reader.readUint8() > 0x01:
                raise CanceledMetException("reader.readUint8() > 0x01")
            self.cancelledFilesSeed = reader.readUint32()

        elif self.version == CanceledMet.OLD_VERSION:
            # Deprecated version of cancelled.met
            pass
        
        elif self.version == CanceledMet.AMULE_VERSION:
            pass
            
        else:
            raise CanceledMetException("Invalied Version: 0x%02X"
                                       % (self.version,));

        if self.cancelledFilesSeed == 0:
            import random
            self.cancelledFilesSeed = random.Random().randint(1,9)

        record_count = reader.readUint32()
        for i in range(0, record_count):
            # Record().loadHashs(reader, loadFileHashOnly=True)
            h = reader.readHash()
            if self.version != CanceledMet.AMULE_VERSION:
                # for compatibility with future versions which may add more data than just the hash
                Record().loadTags(reader)
            if self.version == CanceledMet.OLD_VERSION:
                # convert old real hash to new hashash
                import hashlib
                import sys.byteorder
                d = self.cancelledFilesSeed.to_bytes(4, sys.byteorder)
                d += h
                md5 = hashlib.new("md5", d)
                h = md5.digest()[0:16]
            self.hashs.add(h.hex().upper())
            
    def printDetails(self):
        for h in self.hashs: print(h)
        print("------------------------------------------------")
        pformat("Version:", "0x%02X" % (self.version,))
        pformat("Record Count:", len(self.hashs))

    @staticmethod
    def main()->int:
        import sys
        import argparse
        p = argparse.ArgumentParser()
        p.add_argument(dest="file", nargs=1, help="canceled.met")
        args = p.parse_args(sys.argv[1:])
        try:
            CanceledMet(args.file[0]).printDetails()
            return 0
        except Exception as err:
            print("Exception:", err, file=sys.stderr)
            return 1

