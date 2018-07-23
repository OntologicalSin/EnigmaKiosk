import sqlite3
from files import FileList



class DataBase:

    def __init__(self, fullname):
        # Initialize connection to SQLite3 database and store cursor
        self._connection = sqlite3.connect(fullname)
        self._cursor = self._connection.cursor()

    def select(self, query):
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        return rows

    def execute(self, query):
        self._cursor.execute(query)
        self._connection.commit()


class FileTableManager:

    def __init__(self, db):
        self._db = db

        # Create table for files
        try:
            self._db.execute('CREATE TABLE files (id INTEGER PRIMARY KEY, filename VARCHAR(255), username VARCHAR(255), pages INTEGER, folder VARCHAR(255))')
        except sqlite3.OperationalError:
            # Table already exists
            pass

    def select_all_files(self):
        # Get list of files from database
        rows = self._db.select('SELECT * FROM files ORDER BY id')
        files = FileList(rows)
        return files

    def select_file(self, id):
        # Get entry of file from database
        rows = self._db.select('SELECT * FROM files WHERE id=%d' % (int(id)))
        files = FileList(rows)
        return files[0]

    def insert_file(self, filename, username, pages, folder):
        # Add entry with filename, username, count of pages and folder to database
        self._db.execute('INSERT INTO files (id, filename, username, pages, folder) VALUES (NULL, "%s", "%s", %d, "%s")' % (filename, username, pages, folder))

    def delete_file(self, id):
        # Remove entry of file from database with ID from request
        self._db.execute('DELETE FROM files WHERE id=%d' % (int(id)))

