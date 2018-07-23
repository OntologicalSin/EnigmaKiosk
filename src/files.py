class FileEntry:

    def __init__(self, row):
        self.id = row[0]
        self.filename = row[1]
        self.username = row[2]
        self.pages = row[3]
        self.folder = row[4]


class FileList:

    def __init__(self, rows):
        self._files = []
        self._index = 0

        for row in rows:
            self._files.append(FileEntry(row))

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        self._index += 1
        if len(self._files) >= self._index:
            return self._files[self._index - 1]
        else:
            raise StopIteration

    def __getitem__(self, item):
        try:
            return self._files[item]
        except:
            return None

    def is_empty(self):
        if self._files == []:
            return True
        return False

