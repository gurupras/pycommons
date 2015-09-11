import os
import shutil_helper

class FileEntry(list):
    def __init__(self, name, parent):
        if parent is not None and not isinstance(parent, FileEntry):
            print "Cannot initialize class FileEntry with parent of type '%s'" % (parent.__class__)
            raise Exception
        super(FileEntry, self).__init__()
        self.name    = name
        self.parent   = parent

    def build(self, regex=['*.*']):
        del self[:]
        path = self.path()
        if os.path.isdir(path):
            files, dirs = shutil_helper.get_files(path, regex)
            entries = list(files)
            entries.extend(dirs)
            # Append the current path since ls only returns basenames
            entries = [os.path.join(path, e) for e in entries]
            for entry in entries:
                basename = os.path.basename(entry)
                dirname  = os.path.dirname(entry)
                assert os.path.abspath(path) == os.path.abspath(dirname), \
                        'does not match:\nself   :%s\ndirname:%s' % ( \
                        path, dirname)
                child = FileEntry(basename, self)
                self.append(child)
                if os.path.isdir(entry):
                    child.build(regex)

    def append(self, o):
        # FIXME: Very inefficient to sort on every append()
        super(FileEntry, self).append(o)
        self.sort(key=lambda x: x.name)

    def path(self):
        if self.parent is not None:
            return os.path.join(self.parent.path(), self.name)
        else:
            return self.name

    def __str__(self):
        return self.name
    def __repr__(self):
        if os.path.isfile(self.path()):
            return '%s' % (self.name)
        else:
            return '%s -> %s' % (self.name, super(FileEntry, self).__repr__())

    def isdir(self):
        path = self.path()
        return os.path.isdir(path)

    def isfile(self):
        path = self.path()
        return os.path.isfile(path)

    @staticmethod
    def prefix_tabs(name, tabs):
        retval = ''
        for i in range(tabs):
            retval += '\t'
        retval += name
        return retval

    def pretty_print(self, tabs=0):
        print FileEntry.prefix_tabs(self.name, tabs)
        for child in self:
            child.pretty_print(tabs + 1)

