#!/usr/bin/python3
import os
import io
import sys
import hashlib

class LinkCreator:
    PartSize = 9728000
    PrintPartHashsEnabled = False
    
    def __init__(self, name_, size_):
        if len(name_) == 0 or size_ == 0:
            raise ValueError('Invalid Argument')
        self.name = name_.replace(' ', '_')
        self.size = size_
        self.hash_ = ''
        self.hashlist = []

    def __createPartHash(self, binfile, size_):
        md4 = hashlib.new('md4')
        while size_ > 0:
            d = binfile.read(min(8192, size_))
            md4.update(d)
            size_ -= len(d)
        return md4.digest()
        
    def createFromFile(self, binfile):
        hlist = []
        sz = self.size
        while sz >= LinkCreator.PartSize:
            hlist.append(self.__createPartHash(binfile, LinkCreator.PartSize))
            sz -= LinkCreator.PartSize

        #assert(sz >= 0)
        hlist.append(self.__createPartHash(binfile, sz))

        if len(hlist) > 1:
            md4 = hashlib.new('md4')
            for h in hlist:
                md4.update(h)
                self.hashlist.append(h.hex().upper())
            self.hash_ = md4.hexdigest().upper()
        else:
            self.hash_ = hlist[0].hex().upper()

    def printLink(self, outfile=sys.stdout):
        link = 'ed2k://|file|%s|%s|%s' % (self.name, self.size, self.hash_)
        if LinkCreator.PrintPartHashsEnabled and len(self.hashlist) > 1:
            link += '|p=%s' % (self.hashlist[0],)
            for i in range(1, len(self.hashlist)):
                link += ':%s' % (self.hashlist[i],)
        link += '|/'
        print(link, file=outfile)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("No argument\n")
        exit(1)

    try:
        LinkCreator.PrintPartHashsEnabled = True
        for fpath in sys.argv[1:]:
            l = LinkCreator(os.path.basename(fpath), os.path.getsize(fpath))
            with open(fpath, 'rb') as binfile:
                l.createFromFile(binfile)
            l.printLink()
    except Exception as e:
        print('Exception:', e, file=sys.stderr)
        exit(2)
        
