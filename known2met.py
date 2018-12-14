#!/bin/env python3
#-*- coding: utf-8 -*-
# known2_64.met 格式：
#   [Version ]----------[Version: uint8               ]
#   [HashTree]+---------[RootHash: uint160            ]
#   [HashTree]+     `---[HashCount: uint32            ] 
#       .      `     `--[AllHashs: uint160 * HashCount]
#       .       `-------[RootHash: uint160            ]
#       .           `---[HashCount: uint32            ] 
#       .            `--[AllHashs: uint160 * HashCount]

import sys
from base64 import b32decode, b32encode

VERSION= 0x02
HASH_SIZE = 20
    
class Known2Exception(Exception):
    pass

class Known2_Decode:
    """ 将 known2_64.met 二进制文件转换为文本，通过 sys.stdout 输出 """
    def __init__(self, infile, length, outfile=sys.stdout):
        self.outfile = outfile
        self.infile = infile
        self.length = length
        self.offset = 0

    def decode(self):
        self.processVersion()
        while self.offset < self.length:
            self.processHash()
            count = self.processHashCount()
            while count > 0:
                self.processHash()
                count -= 1
        self.outfile.flush()

    def processVersion(self):
        version = self.infile.read(1)
        if len(version) != 1 or version[0] != VERSION:
            raise Known2Exception("Invalid Version")
        print(version[0], file=self.outfile)
        self.offset += 1

    def processHashCount(self):
        data = self.infile.read(4)
        if len(data) != 4:
            raise Known2Exception("Invalid HASH Count")
        count = int.from_bytes(data, byteorder="little")
        if count == 0:
            raise Known2Exception("Invalid HASH Count")
        print(count, file=self.outfile)
        self.offset += 4
        return count

    def processHash(self):
        aich = self.infile.read(HASH_SIZE)
        if len(aich) != HASH_SIZE:
            raise Known2Exception("Invalid HASH")
        str_ = b32encode(aich).decode()
        assert(len(str_) == 32)
        print(str_, file=self.outfile)
        self.offset += HASH_SIZE


class Known2_Encode:
    """ 将文本文件转换为二进制数据，通过 sys.stdout.buffer 输出 """
    
    def __init__(self, infile, length, outfile=sys.stdout.buffer):
        self.outfile = outfile
        self.infile = infile
        self.length = length
        self.offset = 0

    def encode(self):
        self.processVersion()
        while self.offset < self.length:
            self.processHash()
            count = self.processHashCount()
            while count > 0:
                self.processHash()
                count -= 1
        self.outfile.flush()

    def processVersion(self):
        line = self.infile.readline()
        version = int(line)
        if version != VERSION:
            raise Known2Exception("Invalid Version")
        self.outfile.write(version.to_bytes(1, byteorder="little"))
        self.offset += len(line)

    def processHashCount(self):
        line = self.infile.readline()
        count = int(line)
        if count > 0xFFFFFFFF:
            raise Known2Exception("Invalid HASH Count")
        self.outfile.write(count.to_bytes(4, byteorder="little"))
        self.offset += len(line)
        return count

    def processHash(self):
        line = self.infile.readline()
        if len(line) != 32+1:
            raise Known2Exception("Invalid HASH")
        aich = b32decode(line[0:32])
        if len(aich) != Known2Met.HASH_SIZE:
            raise Known2Exception("Invalid HASH")
        self.outfile.write(aich)
        self.offset += len(line)


class Known2Met:
    @staticmethod
    def main()->int:
        import argparse
        p = argparse.ArgumentParser()
        p.add_argument("-d", dest="d", action="store_true", help="decode know2_64.met")
        p.add_argument("-e", dest="e", action="store_true", help="encode know2_64.txt")
        p.add_argument(dest="file", nargs=1, help="know2_64.met or know2_64.txt")
        args = p.parse_args(sys.argv[1:])
        try:
            import os.path
            filesize = os.path.getsize(args.file[0])
            if filesize == 0:
                print("Empty File", file=sys.stderr)
                return 2

            decode = args.d or (not args.e)
            if decode:
                with open(args.file[0], "rb") as binfile:
                    Known2_Decode(binfile, filesize).decode()  
            else:
                with open(args.file[0], "r") as txtfile:
                    Known2_Encode(txtfile, filesize).encode()
        except Known2Exception as e:
            print("Known2Exception:", e, file=sys.stderr)
            return 3
        except Exception as e:
            print("Exception:", e, file=sys.stderr)
            return 4


if __name__ == "__main__":
    sys.exit(Known2Met.main())
