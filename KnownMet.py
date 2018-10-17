#!/bin/python3
#-*- coding=UTF-8 -*-
import sys
import os
import time
import hashlib

FIXED_TAGS = 15
OLD_MAX_FILE_SIZE = 4290048000

MET_HEADER = 0x0E
MET_HEADER_I64TAGS = 0x0F

PR_LOW = 0
PR_NORMAL = 1
PR_HIGH = 2
PR_VERYHIGH = 3
PR_VERYLOW = 4
PR_AUTO = 5
PR_POWERSHARE = 6

PARTFILE_VERSION = 0xE0
PARTFILE_SPLITTEDVERSION = 0xE1  # For edonkey part files importing.
PARTFILE_VERSION_LARGEFILE = 0xE2

PMT_UNKNOWN = 0
PMT_DEFAULTOLD = 1
PMT_SPLITTED = 2
PMT_NEWOLD = 3
PMT_SHAREAZA = 4
PMT_BADFORMAT = 5

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

FT_FILENAME = 0x01
FT_FILESIZE = 0x02
FT_FILESIZE_HI = 0x3A
FT_FILETYPE = 0x03
FT_FILEFORMAT = 0x04
FT_LASTSEENCOMPLETE = 0x05
FT_TRANSFERRED = 0x08
FT_GAPSTART = 0x09
FT_GAPEND = 0x0A
FT_DESCRIPTION = 0x0B
FT_PARTFILENAME = 0x12
FT_OLDDLPRIORITY = 0x13
FT_STATUS = 0x14
FT_SOURCES = 0x15
FT_PERMISSIONS = 0x16
FT_OLDULPRIORITY = 0x17
FT_DLPRIORITY = 0x18
FT_ULPRIORITY = 0x19
FT_COMPRESSION = 0x1A
FT_CORRUPTED = 0x1B
FT_KADLASTPUBLISHKEY = 0x20
FT_KADLASTPUBLISHSRC = 0x21
FT_FLAGS = 0x22
FT_DL_ACTIVE_TIME = 0x23
FT_CORRUPTEDPARTS = 0x24
FT_DL_PREVIEW = 0x25
FT_KADLASTPUBLISHNOTES = 0x26
FT_AICH_HASH = 0x27
FT_FILEHASH = 0x28
FT_COMPLETE_SOURCES = 0x30
FT_COLLECTIONAUTHOR = 0x31
FT_COLLECTIONAUTHORKEY = 0x32
FT_PUBLISHINFO = 0x33
FT_LASTSHARED = 0x34
FT_AICHHASHSET = 0x35
FT_ATTRANSFERRED = 0x50
FT_ATREQUESTED = 0x51
FT_ATACCEPTED = 0x52
FT_CATEGORY = 0x53
FT_ATTRANSFERREDHI = 0x54
FT_MAXSOURCES = 0x55
FT_NOTCOUNTEDTRANSFERREDLOW = 0x90
FT_NOTCOUNTEDTRANSFERREDHIGH = 0x91
FT_LASTDATAUPDATE = 0x92
FT_MEDIA_ARTIST = 0xD0
FT_MEDIA_ALBUM = 0xD1
FT_MEDIA_TITLE = 0xD2
FT_MEDIA_LENGTH = 0xD3
FT_MEDIA_BITRATE = 0xD4
FT_MEDIA_CODEC = 0xD5
FT_FILECOMMENT = 0xF6
FT_FILERATING = 0xF7

PriorityDict = {
PR_LOW:'PR_LOW',
PR_NORMAL:'PR_NORMAL',
PR_HIGH:'PR_HIGH',
PR_VERYHIGH:'PR_VERYHIGH',
PR_VERYLOW:'PR_VERYLOW',
PR_AUTO:'PR_AUTO',
PR_POWERSHARE:'PR_POWERSHARE'
}

TagTypeDict = {
TAGTYPE_HASH16:'TAGTYPE_HASH16',
TAGTYPE_STRING:'TAGTYPE_STRING',
TAGTYPE_UINT32:'TAGTYPE_UINT32',
TAGTYPE_FLOAT32:'TAGTYPE_FLOAT32',
TAGTYPE_BOOL:'TAGTYPE_BOOL',
TAGTYPE_BOOLARRAY:'TAGTYPE_BOOLARRAY',
TAGTYPE_BLOB:'TAGTYPE_BLOB',
TAGTYPE_UINT16:'TAGTYPE_UINT16',
TAGTYPE_UINT8:'TAGTYPE_UINT8',
TAGTYPE_BSOB:'TAGTYPE_BSOB',
TAGTYPE_UINT64:'TAGTYPE_UINT64'
}

NameIdDict = {
FT_FILENAME:'FT_FILENAME',
FT_FILESIZE:'FT_FILESIZE',
FT_FILESIZE_HI:'FT_FILESIZE_HI',
FT_FILETYPE:'FT_FILETYPE',
FT_FILEFORMAT:'FT_FILEFORMAT',
FT_LASTSEENCOMPLETE:'FT_LASTSEENCOMPLETE',
FT_TRANSFERRED:'FT_TRANSFERRED',
FT_GAPSTART:'FT_GAPSTART',
FT_GAPEND:'FT_GAPEND',
FT_DESCRIPTION:'FT_DESCRIPTION',
FT_PARTFILENAME:'FT_PARTFILENAME',
FT_OLDDLPRIORITY:'FT_OLDDLPRIORITY',
FT_STATUS:'FT_STATUS',
FT_SOURCES:'FT_SOURCES',
FT_PERMISSIONS:'FT_PERMISSIONS',
FT_OLDULPRIORITY:'FT_OLDULPRIORITY',
FT_DLPRIORITY:'FT_DLPRIORITY',
FT_ULPRIORITY:'FT_ULPRIORITY',
FT_COMPRESSION:'FT_COMPRESSION',
FT_CORRUPTED:'FT_CORRUPTED',
FT_KADLASTPUBLISHKEY:'FT_KADLASTPUBLISHKEY',
FT_KADLASTPUBLISHSRC:'FT_KADLASTPUBLISHSRC',
FT_FLAGS:'FT_FLAGS',
FT_DL_ACTIVE_TIME:'FT_DL_ACTIVE_TIME',
FT_CORRUPTEDPARTS:'FT_CORRUPTEDPARTS',
FT_DL_PREVIEW:'FT_DL_PREVIEW',
FT_KADLASTPUBLISHNOTES:'FT_KADLASTPUBLISHNOTES',
FT_AICH_HASH:'FT_AICH_HASH',
FT_FILEHASH:'FT_FILEHASH',
FT_COMPLETE_SOURCES:'FT_COMPLETE_SOURCES',
FT_COLLECTIONAUTHOR:'FT_COLLECTIONAUTHOR',
FT_COLLECTIONAUTHORKEY:'FT_COLLECTIONAUTHORKEY',
FT_PUBLISHINFO:'FT_PUBLISHINFO',
FT_LASTSHARED:'FT_LASTSHARED',
FT_AICHHASHSET:'FT_AICHHASHSET',
FT_ATTRANSFERRED:'FT_ATTRANSFERRED',
FT_ATREQUESTED:'FT_ATREQUESTED',
FT_ATACCEPTED:'FT_ATACCEPTED',
FT_CATEGORY:'FT_CATEGORY',
FT_ATTRANSFERREDHI:'FT_ATTRANSFERREDHI',
FT_MAXSOURCES:'FT_MAXSOURCES',
FT_NOTCOUNTEDTRANSFERREDLOW:'FT_NOTCOUNTEDTRANSFERREDLOW',
FT_NOTCOUNTEDTRANSFERREDHIGH:'FT_NOTCOUNTEDTRANSFERREDHIGH',
FT_LASTDATAUPDATE:'FT_LASTDATAUPDATE',
FT_MEDIA_ARTIST:'FT_MEDIA_ARTIST',
FT_MEDIA_ALBUM:'FT_MEDIA_ALBUM',
FT_MEDIA_TITLE:'FT_MEDIA_TITLE',
FT_MEDIA_LENGTH:'FT_MEDIA_LENGTH',
FT_MEDIA_BITRATE:'FT_MEDIA_BITRATE',
FT_MEDIA_CODEC:'FT_MEDIA_CODEC',
FT_FILECOMMENT:'FT_FILECOMMENT',
FT_FILERATING:'FT_FILERATING'
}

def xAssert(boolean):
    if not boolean:
        raise AssertionError("Assertion Failed At: %s: %s" %
                             (sys._getframe().f_back.f_code.co_name,
                              sys._getframe().f_back.f_lineno))

def print3(label, value, tagname=''):
    print('%-20s %-8s %s' % (label, tagname, value))

    
def formatPriority(key):
    return PriorityDict[key]

def formatElapse(seconds):
    if seconds is None:
        return 'None'
    d = seconds // (3600 * 24)
    h = (seconds % (3600 * 24)) // 3600
    m = ((seconds % (3600 * 24)) % 3600) // 60
    #s = ((seconds % (3600 * 24)) % 3600) % 60
    return '%s Days %s Hours %s Minutes' % (d,h,m)

def formatDateTime(time_secs):
    if time_secs is None:
        return 'None'
    if time_secs == 0:
        return 'Unknown'
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_secs))

def formatSize(size):
    if size is None:
        return 'None'
    if size > 1024**3:
        return '%s (%.2f GiB)' % (size, size / 1024**3)
    elif size > 1024**2:
        return '%s (%.2f MiB)' % (size, size / 1024**2)
    elif size > 1024:
        return '%s (%.2f KiB)' % (size, size / 1024)
    return str(size)

def formatSize2(size):
    if size is None:
        return 'None'
    if size > 1024**3:
        return '%.2f GiB' % (size / 1024**3,)
    elif size > 1024**2:
        return '%.2f MiB' % (size / 1024**2,)
    elif size > 1024:
        return '%.2f KiB' % (size / 1024,)
    return str(size)

class OpenForReadBinaryOnly:
    def __init__(self, filepath):
        self.reader = open(filepath, 'rb')

    def close(self):
        self.reader.close()

    def read(self, len_):
        d = self.reader.read(len_)
        xAssert(len(d) == len_)
        return d
        
    def readUint8(self):
        return int.from_bytes(self.read(1), byteorder='little')
    def readUint16(self):
        return int.from_bytes(self.read(2), byteorder='little')
    def readUint32(self):
        return int.from_bytes(self.read(4), byteorder='little')
    def readUint64(self):
        return int.from_bytes(self.read(8), byteorder='little')
    def readFloat32(self):
        return int.from_bytes(self.read(4), byteorder='big')
    def readHash(self):
        return self.read(16)
    def readUtf8(self, len_):
        return self.read(len_).decode('utf-8')

    def seek(self, offset, whence=0):
        return self.reader.seek(offset, whence)
    def tell(self):
        return self.reader.tell()
    
class Gap:
    InvalidValue = 0xFFFFFFFFFFFFFFFF
    def __init__(self):
        self.start = Gap.InvalidValue
        self.end = Gap.InvalidValue
        
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
            reader.read(1)
            self.value = 'TAGTYPE_BLOB'
            
        elif self.type_ == TAGTYPE_BOOLARRAY:
            len_ = reader.readUint16()
            # 07-Apr-2004: eMule versions prior to 0.42e.29 used the formula: "(len_+7)//8"! warning This seems to be off by one! 8 // 8 + 1 == 2, etc.
            reader.seek(len_//8 + 1, 1)
            self.value = 'TAGTYPE_BOOLARRAY'
            
        elif self.type_ == TAGTYPE_BLOB:
            reader.seek(reader.readUint32(), 1)
            self.value = 'TAGTYPE_BLOB'
            
        else:
            raise Exception('Unknown tag type: %s' % (self.type_,) )
            

    def isInt(self):
        return self.type_ in (TAGTYPE_UINT64, TAGTYPE_UINT32,
                              TAGTYPE_UINT16, TAGTYPE_UINT8)
    
    def isStr(self):
        return self.type_ == TAGTYPE_STRING
    
class Record:
    ModifTime = 1
    FileHash = 2
    PartHashs = 3
    FileSize = 4
    def __init__(self, reader):
        self.head = {}
        self.body = {}
        self.taglist = []
        self.gaplist = []
        self.__loadModifTime(reader)
        self.__loadHashs(reader)
        self.__loadTags(reader)

    def getFileSize(self):
        list_ = self.body.get(FT_FILESIZE)
        return int(list_.split()[0]) if list_ else 0
        
    def isLargeFile(self):
        return self.getFileSize() > OLD_MAX_IN_SIZE

    def getFileHash(self):
        return self.head[Record.FileHash].hex().upper()

    def __loadModifTime(self, reader):
        self.head[Record.ModifTime] = reader.readUint32()

    def __loadHashs(self, reader):
        self.head[Record.FileHash] = reader.readHash()
        n = reader.readUint16()
        self.head[Record.PartHashs] = [reader.readHash() for _ in range(0,n)]
        
        if n == 1:
            xAssert(self.head[Record.FileHash] == self.head[Record.PartHashs][0])
        elif n > 1:
            md4 = hashlib.new('md4')
            for h in self.head[Record.PartHashs]:
                md4.update(h)
            xAssert(self.head[Record.FileHash] == md4.digest())

    def __loadTags(self, reader):
        gdict = {}
        tagCount = reader.readUint32()
        
        for _ in range(0, tagCount):
            tag = Tag(reader)
            if tag.name_id is None:
                self.taglist.append(tag)
                
            elif tag.name_id == FT_FILENAME:
                xAssert(tag.isStr())
                self.body.setdefault(tag.name_id, tag.value)

            elif tag.name_id == FT_PARTFILENAME:
                xAssert(tag.isStr())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_FILESIZE,FT_COMPRESSION,FT_TRANSFERRED):
                xAssert(tag.isInt())
                self.body[tag.name_id] = formatSize(tag.value)

            elif tag.name_id in (FT_LASTSEENCOMPLETE,FT_LASTDATAUPDATE):
                xAssert(tag.isInt())
                self.body[tag.name_id] = formatDateTime(tag.value)

            elif tag.name_id == FT_DL_ACTIVE_TIME:
                xAssert(tag.isInt())
                self.body[tag.name_id] = formatElapse(tag.value)

            elif tag.name_id == FT_STATUS:
                xAssert(tag.isInt())
                if tag.value == 0:
                    self.body[tag.name_id] = 'Downloading'
                else:
                    self.body[tag.name_id] = 'Paused Or Stopped'

            elif tag.name_id == FT_FILETYPE:
                xAssert(tag.isStr())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_CORRUPTED, FT_CATEGORY, FT_MAXSOURCES):
                xAssert(tag.isInt())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_DLPRIORITY, FT_OLDDLPRIORITY):
                xAssert(tag.isInt())
                v = tag.value
                if v == PR_AUTO: v = PR_HIGH
                elif not v in (PR_LOW,PR_NORMAL,PR_HIGH): v = PR_NORMAL
                self.body[FT_DLPRIORITY] = formatPriority(v)
                    
            elif tag.name_id in (FT_ULPRIORITY, FT_OLDULPRIORITY):
                xAssert(tag.isInt())
                v = tag.value
                if v == PR_AUTO: v = PR_HIGH
                elif not v in (PR_LOW,PR_NORMAL,PR_HIGH): v = PR_NORMAL
                self.body[FT_ULPRIORITY] = formatPriority(v)

            elif tag.name_id == FT_KADLASTPUBLISHSRC:
                xAssert(tag.isInt())
                ### SetLastPublishTimeKadSrc(tag.value, IPv4Address(0))
                self.body[tag.name_id] = formatDateTime(tag.value)

            elif tag.name_id == FT_KADLASTPUBLISHNOTES:
                xAssert(tag.isInt())
                ### SetLastPublishTimeKadNotes(tag.value)
                self.body[tag.name_id] = formatDateTime(tag.value)

            elif tag.name_id == FT_DL_PREVIEW:
                xAssert(tag.isInt())
                ### SetPreviewPrio(((tag->GetInt() >> 0) & 0x01) == 1);
		### SetPauseOnPreview(((tag->GetInt() >> 1) & 0x01) == 1);
                # TODO
                self.body[tag.name_id] = tag.value
                
            elif tag.name_id == FT_ATREQUESTED:
                xAssert(tag.isInt())
                ### statistic.SetAllTimeRequests(tag.value)
                self.body[tag.name_id] = formatSize(tag.value)
                
            elif tag.name_id == FT_ATACCEPTED:
                xAssert(tag.isInt())
                ### statistic.SetAllTimeAccepts(tag.value)
                self.body[tag.name_id] = formatSize(tag.value)

            elif tag.name_id == FT_ATTRANSFERRED:
                xAssert(tag.isInt())
                ### statistic.SetAllTimeTransferred(tag.value)
                self.body[tag.name_id] = formatSize(tag.value)
                
            elif tag.name_id == FT_ATTRANSFERREDHI:
                xAssert(tag.isInt())
                ### low = statistic.GetAllTimeTransferred()
                ### hi = tag.value << 32
                ### statistic.SetAllTimeTransferred(low + hi)
                # TODO
                self.body[tag.name_id] = str(tag.value)
                        
            elif tag.name_id == FT_CORRUPTEDPARTS:
                xAssert(tag.isStr())
                self.body[tag.name_id] = tag.value
            
            elif tag.name_id == FT_AICH_HASH:
                xAssert(tag.isStr())
                xAssert(len(tag.value) == 32)
                xAssert(tag.value.isalnum())
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_AICHHASHSET:
                xAssert(tag.type_ == TAGTYPE_BLOB)
                # TODO
                xAssert(False)

            elif tag.name_id in (FT_PERMISSIONS, FT_KADLASTPUBLISHKEY):
                ### old tags: as long as they are not needed,
                ### take the chance to purge them.
                xAssert(tag.isInt())
                self.body[tag.name_id] = tag.value

            else:
                if (tag.name_id == 0 and tag.isInt()
                    and tag.name != None and len(tag.name) > 1
                    and tag.name[0] in (FT_GAPSTART, FT_GAPEND)):
                    key = int(tag.name[1:])
                    xAssert(key >= 0)
                    gap = gdict.setdefault(key, Gap())
                    if tag.name[0] == FT_GAPSTART:
                        gap.start = tag.value
                    else:
                        gap.end = tag.value
                else:
                    self.taglist.append(tag)

            if 0:
                print('%-20s %-15s %-8s %s' %
                      (NameIdDict.get(tag.name_id),
                       TagTypeDict[tag.type_],
                       tag.name,
                       self.body.get(tag.name_id, tag.value)))

        #TODO
        self.gaplist = sorted(gdict.values(), key=lambda x:x.start)
            
    def printEd2kLink(self):
        print('ed2k://|file|%s|%s|%s|/' %
              (self.body[FT_FILENAME].replace(' ', '_'),
               self.getFileSize(),
               self.getFileHash()) )

    def printDetails(self):
        print3('ModifTime:', formatDateTime(self.head.get(Record.ModifTime)))
        print3('FileHash:', self.getFileHash())
        print3('PartHashCount:', len(self.head[Record.PartHashs]))
        for k in self.body.keys():
            v = self.body[k]
            print3(NameIdDict[k], v)
        #print3('OtherTagCount:', len(self.taglist))
        #for tag in self.taglist: print3('', tag.value, tagname=tag.name)
        #print3('NeedsRangeCount:', len(self.gaplist))

class KnownMet:
    PrintLinkOnlyEnabled = False
    Version = 0
    Count = 1
    def __init__(self, metpath):
        self.head = [0, 0]
        self.body = []
        reader = OpenForReadBinaryOnly(metpath)
        self.__loadFromFile(reader)
        reader.close()
    
    def __loadFromFile(self, reader):
        start_pos = reader.tell()
        self.head[KnownMet.Version] = reader.readUint8()
        if not self.head[KnownMet.Version] in (MET_HEADER,
                                               MET_HEADER_I64TAGS):
            print('Version:', hex(self.head[KnownMet.Version]), file=sys.stderr)
            raise Exception('Invailed Version')
        self.head[KnownMet.Count] = reader.readUint32()
        self.__loadRecords(reader)

    def __loadRecords(self, reader):
        for _ in range(0, self.head[KnownMet.Count]):
            self.body.append(Record(reader))

    def printRecords(self):
        xAssert(self.head[KnownMet.Count] == len(self.body))
        for record in self.body:
            if KnownMet.PrintLinkOnlyEnabled:
                record.printEd2kLink()
            else:
                record.printDetails()
                print('-' * 60)

        if not KnownMet.PrintLinkOnlyEnabled:
            print3('KnownMetVersion:', hex(self.head[KnownMet.Version]))
            print3('RecordCount:', self.head[KnownMet.Count])
    
if __name__ == '__main__':
    def usage(appName, exitCode=0):
        print(appNeme, '[-h|-l] <known.met>', file=sys.stderr)
        exit(exitCode)

    try:
        if len(sys.argv) < 2:
            print('No Argument', file=sys.stderr)
            usage(sys.argv[0], 1)

        fpath = ''
        for arg in sys.argv[1:]:
            if arg == '-h':
                usage(sys.argv[0])
            elif arg == '-l':
                KnownMet.PrintLinkOnlyEnabled = True
            else:
                fpath = arg
            
        km = KnownMet(fpath)
        km.printRecords()
              
    except Exception as e:
        print('Exception:', e, file=sys.stderr)
        exit(2)
