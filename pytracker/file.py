import os

from . import str_hash as h


class File:
    def __init__(self, target_file):
        self.file = target_file

    def exists(self):
        return os.path.isfile(self.file)

    def path(self):
        return self.file

    def md5_hash(self):
        with open(self.file, 'rb') as reader:
            return h.md5_hash(reader.read())
        return None


class Finder:
    def __init__(self):
        pass

    @staticmethod
    def find_extension(extension, target):
        """
        Find all files in specific directory
        with specific extensio
        @todo - optimise
        """
        found = []
        for root, subdirs, files in os.walk(target):
            for f in files:
                abs_file = os.path.join(root, f)
                if abs_file.endswith(extension):
                    found.append(File(abs_file))

        return found
