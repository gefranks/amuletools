#!/usr/bin/python3

# known2_64.met 格式：
#   [Version ]----------[Version: uint8               ]
#   [HashTree]+---------[RootHash: uint160            ]
#   [HashTree]+     `---[HashCount: uint32            ] 
#       .      `     `--[AllHashs: uint160 * HashCount]
#       .       `-------[RootHash: uint160            ]
#       .           `---[HashCount: uint32            ] 
#       .            `--[AllHashs: uint160 * HashCount]

import os
import sys
import base64

class Known2Exception(Exception): pass

class Known2Met:
    """ 将 known2_64.met 二进制文件转换为文本，通过 sys.stdout 输出 """
    
    VERSION = 0x02
    HASH_SIZE = 20
    
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
        if len(version) != 1 or version[0] != Known2Met.VERSION:
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
        aich = self.infile.read(Known2Met.HASH_SIZE)
        if len(aich) != Known2Met.HASH_SIZE:
            raise Known2Exception("Invalid HASH")
        str_ = base64.b32encode(aich).decode()
        assert(len(str_) == 32)
        print(str_, file=self.outfile)
        self.offset += Known2Met.HASH_SIZE


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
        if version != Known2Met.VERSION:
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
        aich = base64.b32decode(line[0:32])
        if len(aich) != Known2Met.HASH_SIZE:
            raise Known2Exception("Invalid HASH")
        self.outfile.write(aich)
        self.offset += len(line)


if __name__ == "__main__":

    filepath = None
    decode = True
    for arg in sys.argv[1:]:
        if arg == "-d":
            decode = True
        elif arg == "-e":
            decode = False
        else:
            filepath = arg
            
    if filepath is None:
        print("No Argument", file=sys.stderr)
        exit(1)

    try:
        filesize = os.path.getsize(filepath)
        if filesize == 0:
            print("Empty File", file=sys.stderr)
            exit(2)
            
        if decode:
            with open(filepath, "rb") as binfile:
                km = Known2Met(binfile, filesize)
                km.decode()  
        else:
            with open(filepath, "r") as txtfile:
                ke = Known2_Encode(txtfile, filesize)
                ke.encode()

    except Known2Exception as e:
        print("Known2Exception:", e, file=sys.stderr)
        exit(3)
    except Exception as e:
        print("Exception:", e, file=sys.stderr)
        exit(4)
