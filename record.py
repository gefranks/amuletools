#-*- coding: utf-8 -*-
from constant import *
from function import formatDateTime, formatSize
from tag import Tag

class Area:
    InvalidPosition = 0xFFFFFFFFFFFFFFFF
    def __init__(self):
        self.start = Area.InvalidPosition
        self.end = Area.InvalidPosition
    
class Record:
    ModifTime = 1
    FileHash = 2
    PartHashs = 3
    FileSize = 4
    
    def __init__(self):
        self.head = {}
        self.body = {}
        self.taglist = []
        self.arealist = [] # incomplete

    def getFileSize(self):
        return self.body[FT_FILESIZE]
        
    def isLargeFile(self):
        return self.getFileSize() > OLD_MAX_IN_SIZE

    def getFileHash(self)->str:
        return self.head[Record.FileHash].hex().upper()

    def getAichHash(self)->str:
        return self.body.get(FT_AICH_HASH, "None")

    def getFileName(self):
        return self.body[FT_FILENAME].strip().replace(" ", "_")

    def getPartName(self)->str:
        return self.body.get(FT_PARTFILENAME, "None")

    def getFormatModifTime(self):
        return formatDateTime(self.head.get(Record.ModifTime, 0))

    def getFormatLastSeenComplete(self):
        return formatDateTime(self.body.get(FT_LASTSEENCOMPLETE, 0))

    def getFormatProgress(self):
        fsize = self.getFileSize()
        complete = fsize
        for area in self.arealist:
            complete -= area.end - area.start
        assert(complete >= 0)
        if complete == fsize:
            return "100%% (%s)" % (formatSize(fsize),)
        percent = "%.2f" % (complete*100/fsize,)
        if percent.startswith("100"):
            percent = "99.99"
        return "%s%% (%s/%s)" % (percent, formatSize(complete), formatSize(fsize))
    
    def getEd2kPartCount(self):
        return len(self.head[Record.PartHashs])

    def getEd2kLink(self):
        return "ed2k://|file|%s|%s|%s|/" % (self.getFileName(),
                                            self.getFileSize(),
                                            self.getFileHash())

    def load(self, reader):
        self.loadModifTime(reader)
        self.loadHashs(reader)
        self.loadTags(reader)
    
    def loadModifTime(self, reader):
        self.head[Record.ModifTime] = reader.readUint32()

    def loadHashs(self, reader, loadFileHashOnly=False):
        self.head[Record.FileHash] = reader.readHash()
        self.head[Record.PartHashs] = []
        if loadFileHashOnly:
            return
        hashcount = reader.readUint16()
        hashlist = [reader.readHash() for _ in range(0, hashcount)]
        if hashcount > 1:
            import hashlib
            md4 = hashlib.new("md4")
            for h in hashlist: md4.update(h)
            assert(self.head[Record.FileHash] == md4.digest())
            self.head[Record.PartHashs] = hashlist
        elif hashcount == 1:
            assert(self.head[Record.FileHash] == hashlist[0])
            self.head[Record.PartHashs] = hashlist
        else:
            pass

    def loadTags(self, reader, isnewstyle=False, partmettype=PMT_DEFAULTOLD):
        areadict = {}
        tagcount = reader.readUint32()
        for _ in range(0, tagcount):
            tag = Tag(reader)
            if tag.name_id is None:
                self.taglist.append(tag)
                
            elif tag.name_id == FT_FILENAME:
                assert(tag.isStr())
                self.body.setdefault(tag.name_id, tag.value)

            elif tag.name_id == FT_PARTFILENAME:
                assert(tag.isStr())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_FILESIZE,FT_COMPRESSION,FT_TRANSFERRED):
                assert(tag.isInt())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_LASTSEENCOMPLETE,FT_LASTDATAUPDATE):
                assert(tag.isInt())
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_DL_ACTIVE_TIME:
                assert(tag.isInt())
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_STATUS:
                assert(tag.isInt())
                if tag.value == 0:
                    self.body[tag.name_id] = "Downloading"
                else:
                    self.body[tag.name_id] = "Paused Or Stopped"

            elif tag.name_id == FT_FILETYPE:
                assert(tag.isStr())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_CORRUPTED, FT_CATEGORY, FT_MAXSOURCES):
                assert(tag.isInt())
                self.body[tag.name_id] = tag.value

            elif tag.name_id in (FT_DLPRIORITY, FT_OLDDLPRIORITY):
                assert(tag.isInt())
                v = tag.value
                if not isnewstyle:
                    if v == PR_AUTO:
                        v = PR_HIGH
                    elif not v in (PR_LOW,PR_NORMAL,PR_HIGH):
                        v = PR_NORMAL
                self.body[FT_DLPRIORITY] = v
                    
            elif tag.name_id in (FT_ULPRIORITY, FT_OLDULPRIORITY):
                assert(tag.isInt())
                v = tag.value
                if not isnewstyle:
                    if v == PR_AUTO:
                        v = PR_HIGH
                    elif not v in (PR_LOW,PR_NORMAL,PR_HIGH):
                        v = PR_NORMAL
                self.body[FT_ULPRIORITY] = v

            elif tag.name_id == FT_KADLASTPUBLISHSRC:
                assert(tag.isInt())
                ### SetLastPublishTimeKadSrc(tag.value, IPv4Address(0))
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_KADLASTPUBLISHNOTES:
                assert(tag.isInt())
                ### SetLastPublishTimeKadNotes(tag.value)
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_DL_PREVIEW:
                assert(tag.isInt())
                ### SetPreviewPrio(((tag->GetInt() >> 0) & 0x01) == 1);
		### SetPauseOnPreview(((tag->GetInt() >> 1) & 0x01) == 1);
                # TODO
                self.body[tag.name_id] = tag.value
                
            elif tag.name_id == FT_ATREQUESTED:
                assert(tag.isInt())
                ### statistic.SetAllTimeRequests(tag.value)
                self.body[tag.name_id] = tag.value
                
            elif tag.name_id == FT_ATACCEPTED:
                assert(tag.isInt())
                ### statistic.SetAllTimeAccepts(tag.value)
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_ATTRANSFERRED:
                assert(tag.isInt())
                ### statistic.SetAllTimeTransferred(tag.value)
                self.body[tag.name_id] = tag.value
                
            elif tag.name_id == FT_ATTRANSFERREDHI:
                assert(tag.isInt())
                ### low = statistic.GetAllTimeTransferred()
                ### hi = tag.value << 32
                ### statistic.SetAllTimeTransferred(low + hi)
                # TODO
                self.body[tag.name_id] = str(tag.value)
                        
            elif tag.name_id == FT_CORRUPTEDPARTS:
                assert(tag.isStr())
                self.body[tag.name_id] = tag.value
            
            elif tag.name_id == FT_AICH_HASH:
                assert(tag.isStr())
                assert(len(tag.value) == 32)
                assert(tag.value.isalnum())
                self.body[tag.name_id] = tag.value

            elif tag.name_id == FT_AICHHASHSET:
                assert(tag.type_ == TAGTYPE_BLOB)
                # TODO
                # print(tag.value, file=sys.stderr)

            elif tag.name_id in (FT_PERMISSIONS, FT_KADLASTPUBLISHKEY):
                ### old tags: as long as they are not needed,
                ### take the chance to purge them.
                assert(tag.isInt())
                self.body[tag.name_id] = tag.value

            else:
                if (tag.name_id == 0 and tag.isInt()
                    and tag.name != None and len(tag.name) > 1
                    and tag.name[0] in (FT_GAPSTART, FT_GAPEND)):
                    key = int(tag.name[1:])
                    assert(key >= 0)
                    area = areadict.setdefault(key, Area())
                    if tag.name[0] == FT_GAPSTART:
                        area.start = tag.value
                    else:
                        area.end = tag.value
                else:
                    self.taglist.append(tag)

            if 0:
                if tag.name:
                    pformat("Tag Name:", tag.name)
                else:
                    pformat("Tag Name ID:", NameIdDict[tag.name_id])
                pformat("Tag Type:", TagTypeDict[tag.type_])
                pformat("Tag value:", tag.value)
                print("---------------------------------------------")

        #TODO
        self.arealist = sorted(areadict.values(), key=lambda x:x.start)
