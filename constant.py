#-*- coding: utf-8 -*-

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
PR_LOW:"PR_LOW",
PR_NORMAL:"PR_NORMAL",
PR_HIGH:"PR_HIGH",
PR_VERYHIGH:"PR_VERYHIGH",
PR_VERYLOW:"PR_VERYLOW",
PR_AUTO:"PR_AUTO",
PR_POWERSHARE:"PR_POWERSHARE"
}

TagTypeDict = {
TAGTYPE_HASH16:"TAGTYPE_HASH16",
TAGTYPE_STRING:"TAGTYPE_STRING",
TAGTYPE_UINT32:"TAGTYPE_UINT32",
TAGTYPE_FLOAT32:"TAGTYPE_FLOAT32",
TAGTYPE_BOOL:"TAGTYPE_BOOL",
TAGTYPE_BOOLARRAY:"TAGTYPE_BOOLARRAY",
TAGTYPE_BLOB:"TAGTYPE_BLOB",
TAGTYPE_UINT16:"TAGTYPE_UINT16",
TAGTYPE_UINT8:"TAGTYPE_UINT8",
TAGTYPE_BSOB:"TAGTYPE_BSOB",
TAGTYPE_UINT64:"TAGTYPE_UINT64"
}

NameIdDict = {
FT_FILENAME:"FT_FILENAME",
FT_FILESIZE:"FT_FILESIZE",
FT_FILESIZE_HI:"FT_FILESIZE_HI",
FT_FILETYPE:"FT_FILETYPE",
FT_FILEFORMAT:"FT_FILEFORMAT",
FT_LASTSEENCOMPLETE:"FT_LASTSEENCOMPLETE",
FT_TRANSFERRED:"FT_TRANSFERRED",
FT_GAPSTART:"FT_GAPSTART",
FT_GAPEND:"FT_GAPEND",
FT_DESCRIPTION:"FT_DESCRIPTION",
FT_PARTFILENAME:"FT_PARTFILENAME",
FT_OLDDLPRIORITY:"FT_OLDDLPRIORITY",
FT_STATUS:"FT_STATUS",
FT_SOURCES:"FT_SOURCES",
FT_PERMISSIONS:"FT_PERMISSIONS",
FT_OLDULPRIORITY:"FT_OLDULPRIORITY",
FT_DLPRIORITY:"FT_DLPRIORITY",
FT_ULPRIORITY:"FT_ULPRIORITY",
FT_COMPRESSION:"FT_COMPRESSION",
FT_CORRUPTED:"FT_CORRUPTED",
FT_KADLASTPUBLISHKEY:"FT_KADLASTPUBLISHKEY",
FT_KADLASTPUBLISHSRC:"FT_KADLASTPUBLISHSRC",
FT_FLAGS:"FT_FLAGS",
FT_DL_ACTIVE_TIME:"FT_DL_ACTIVE_TIME",
FT_CORRUPTEDPARTS:"FT_CORRUPTEDPARTS",
FT_DL_PREVIEW:"FT_DL_PREVIEW",
FT_KADLASTPUBLISHNOTES:"FT_KADLASTPUBLISHNOTES",
FT_AICH_HASH:"FT_AICH_HASH",
FT_FILEHASH:"FT_FILEHASH",
FT_COMPLETE_SOURCES:"FT_COMPLETE_SOURCES",
FT_COLLECTIONAUTHOR:"FT_COLLECTIONAUTHOR",
FT_COLLECTIONAUTHORKEY:"FT_COLLECTIONAUTHORKEY",
FT_PUBLISHINFO:"FT_PUBLISHINFO",
FT_LASTSHARED:"FT_LASTSHARED",
FT_AICHHASHSET:"FT_AICHHASHSET",
FT_ATTRANSFERRED:"FT_ATTRANSFERRED",
FT_ATREQUESTED:"FT_ATREQUESTED",
FT_ATACCEPTED:"FT_ATACCEPTED",
FT_CATEGORY:"FT_CATEGORY",
FT_ATTRANSFERREDHI:"FT_ATTRANSFERREDHI",
FT_MAXSOURCES:"FT_MAXSOURCES",
FT_NOTCOUNTEDTRANSFERREDLOW:"FT_NOTCOUNTEDTRANSFERREDLOW",
FT_NOTCOUNTEDTRANSFERREDHIGH:"FT_NOTCOUNTEDTRANSFERREDHIGH",
FT_LASTDATAUPDATE:"FT_LASTDATAUPDATE",
FT_MEDIA_ARTIST:"FT_MEDIA_ARTIST",
FT_MEDIA_ALBUM:"FT_MEDIA_ALBUM",
FT_MEDIA_TITLE:"FT_MEDIA_TITLE",
FT_MEDIA_LENGTH:"FT_MEDIA_LENGTH",
FT_MEDIA_BITRATE:"FT_MEDIA_BITRATE",
FT_MEDIA_CODEC:"FT_MEDIA_CODEC",
FT_FILECOMMENT:"FT_FILECOMMENT",
FT_FILERATING:"FT_FILERATING"
}
