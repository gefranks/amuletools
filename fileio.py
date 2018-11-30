#-*- coding: utf-8 -*-
import io

class FileIOInvalidDataError(Exception):
    pass

class FileIO(io.FileIO):
    def __init__(self, path, mode="rb"):
        super().__init__(path, mode)
        
    def __readData(self, len_, mssage):
        d = super().read(len_)
        if len(d) != len_:
            raise FileIOInvalidDataError(message)
        return d

    def readData(self, len_):
        return self.__readData(len_, "FileIO.readData")
    def readUint8(self):
        return int.from_bytes(self.__readData(1, "FileIO.readUint8"), byteorder="little")
    def readUint16(self):
        return int.from_bytes(self.__readData(2, "FileIO.readUint16"), byteorder="little")
    def readUint32(self):
        return int.from_bytes(self.__readData(4, "FileIO.readUint32"), byteorder="little")
    def readUint64(self):
        return int.from_bytes(self.__readData(8, "FileIO.readUint64"), byteorder="little")
    def readFloat32(self):
        return int.from_bytes(self.__readData(4, "FileIO.readUint4"), byteorder="big")
    def readHash(self):
        return self.__readData(16, "FileIO.readHash")
    def readUtf8(self, len_):
        return self.__readData(len_, "FileIO.readUtf8").decode("utf-8")
    def readUtf16(self, len_):
        return self.__readData(len_, "FileIO.readUtf16").decode("utf-16-le")
