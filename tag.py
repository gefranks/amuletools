#-*- coding: utf-8 -*-
from .constant import *

class UnknowTagError(Exception):
    pass
        
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
            datasize = reader.readUint16()
            if datasize == 1:
                self.name_id = reader.readUint8()
            else:
                self.name_id = 0
                self.name = reader.readData(datasize)

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
            raise UnknowTagError("Unknown tag type: %s" % (self.type_,) )

    def isInt(self):
        return self.type_ in (TAGTYPE_UINT64, TAGTYPE_UINT32,
                              TAGTYPE_UINT16, TAGTYPE_UINT8)
    
    def isStr(self):
        return self.type_ == TAGTYPE_STRING
