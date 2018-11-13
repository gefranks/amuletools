#!/bin/python3
import sys
import io

TAGTYPE_HASH16 = 0x01
TAGTYPE_STRING = 0x02
TAGTYPE_UINT32 = 0x03
TAGTYPE_FLOAT32	= 0x04
TAGTYPE_BOOL = 0x05
TAGTYPE_BOOLARRAY = 0x06
TAGTYPE_BLOB = 0x07
TAGTYPE_UINT16 = 0x08
TAGTYPE_UINT8 = 0x09
TAGTYPE_BSOB = 0x0A
TAGTYPE_UINT64 = 0x0B
TAGTYPE_STR1 = 0x11
TAGTYPE_STR16 = TAGTYPE_STR1 + 15

def xAssert(boolean):
    if not boolean:
        raise AssertionError("Assertion Failed At: %s: %s" %
                             (sys._getframe().f_back.f_code.co_name,
                              sys._getframe().f_back.f_lineno))

    
class OpenForReadBinaryOnly(io.FileIO):
    def __init__(self, path):
        super().__init__(path, "rb")

    def read(self, len_):
        d = super().read(len_)
        xAssert(len(d) == len_)
        return d
        
    def readUint8(self):
        return int.from_bytes(self.read(1), byteorder="little")
    def readUint16(self):
        return int.from_bytes(self.read(2), byteorder="little")
    def readUint32(self):
        return int.from_bytes(self.read(4), byteorder="little")
    def readUint64(self):
        return int.from_bytes(self.read(8), byteorder="little")
    def readFloat32(self):
        return int.from_bytes(self.read(4), byteorder="big")
    def readHash(self):
        return self.read(16)
    def readUtf8(self, len_):
        return self.read(len_).decode("utf-8")
    def readUtf16(self, len_):
        return self.read(len_).decode("utf-16-le")
    
class Tag:    
    def __init__(self, reader):
        self.name_id = 0
        self.name = None
        self.value = None
        self.type_ = reader.readUint8()
        self.__readNameID(reader)
        self.__readValue(reader)

    def __readNameID(self, reader):
        if self.type_ & 0x80:
            self.type_ &= 0x7F
            self.name_id = reader.readUint8()
        else:
            n = reader.readUint16()
            if n == 1:
                self.name_id = reader.readUint8()
            else:
                self.name_id = 0
                self.name = reader.read(n)
                
    def __readValue(self, reader):
        if self.type_ == TAGTYPE_STRING:
            self.value = reader.readUtf8(reader.readUint16())

        elif TAGTYPE_STR1 <= self.type_ <= TAGTYPE_STR16:
            self.value = reader.readUtf8(self.type_ - TAGTYPE_STR1 + 1)
            self.type_ = TAGTYPE_STRING
    
        elif self.type_ == TAGTYPE_UINT8:
            self.value = reader.readUint8()
            # self.type_ = TAGTYPE_UINT32

        elif self.type_ == TAGTYPE_UINT16:
            self.value = reader.readUint16()
            # self.type_ = TAGTYPE_UINT32
            
        elif self.type_ == TAGTYPE_UINT32:
            self.value = reader.readUint32()
            
        elif self.type_ == TAGTYPE_UINT64:
            self.value = reader.readUint64()
        
        elif self.type_ == TAGTYPE_FLOAT32:
            self.value = reader.readFloat32()
            
        elif self.type_ == TAGTYPE_HASH16:
            self.value = reader.readHash()
            
        elif self.type_ == TAGTYPE_BOOL:
            self.value = reader.readUint8()
            
        elif self.type_ == TAGTYPE_BOOLARRAY:
            len_ = reader.readUint16()
            # 07-Apr-2004: eMule versions prior to 0.42e.29 used the formula: "(len_+7)//8"! warning This seems to be off by one! 8 // 8 + 1 == 2, etc.
            reader.seek(len_//8 + 1, 1)
            # TODO
            self.value = "None"
            
        elif self.type_ == TAGTYPE_BLOB:
            reader.seek(reader.readUint32(), 1)
            # TODO
            self.value = "None"
            
        else:
            raise Exception("Unknown tag type: 0x%02x" % (self.type_,))


class CanceledMetException(Exception):
    pass

class CanceledMet:
    AMULE_VERSION = 0x21
    VERSION = 0x0F
    OLD_VERSION = 0x0E
    
    def __init__(self, path):
        self.cancelledFilesSeed = 0
        self.version = 0
        self.records = frozenset()

        with OpenForReadBinaryOnly(path) as file_:
            self.__load(file_)
            xAssert(not io.FileIO.read(file_, 1))

    def __load(self, file_):
        self.version = file_.readUint8()
        if self.version == CanceledMet.VERSION:
            if file_.readUint8() > 0x01:
                raise CanceledMetException("file_.readUint8() > 0x01")
            self.cancelledFilesSeed = file_.readUint32()

        elif self.version == CanceledMet.OLD_VERSION:
            # Deprecated version of cancelled.met
            pass
        
        elif self.version == CanceledMet.AMULE_VERSION:
            pass
            
        else:
            raise CanceledMetException("Invalied Version: 0x%02x"
                                        % (self.version,));

        if self.cancelledFilesSeed == 0:
            import random
            self.cancelledFilesSeed = random.Random().randint(1,9)

        hashs = []
        recordCount = file_.readUint32()
        for i in range(0, recordCount):
            hashs.append(file_.readHash())
            if self.version != CanceledMet.AMULE_VERSION:
                tagCount = file_.readUint8()
                # for compatibility with future versions which may add more data than just the hash
                for j in range(0, tagCount): Tag(file_)
            if self.version == CanceledMet.OLD_VERSION:
                # convert old real hash to new hashash
                import hashlib
                d = self.cancelledFilesSeed.to_bytes(4, sys.byteorder)
                d += hashs[i]
                md5 = hashlib.md5()
                md5.update(d)
                hashs[i] = md5.digest()[0:16]
                
        self.records = frozenset(hashs)

    def __p(self, label, value):
        print("%-30s%s" % (label, value))
            
    def printDetails(self):
        for hash_ in self.records:
            print(hash_.hex().upper())
            
        self.__p("Version:", "0x%02x" % (self.version,))
        self.__p("Record Count:", len(self.records))
            
        
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No Argument", file=sys.stderr)
        sys.exit(1)

    try:
        cm = CanceledMet(sys.argv[1])
        cm.printDetails()
        sys.exit(0)
    except CanceledMetException as e:
        print("CanceledMetException:", e, file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print("Exception:", e, file=sys.stderr)
        sys.exit(3)
