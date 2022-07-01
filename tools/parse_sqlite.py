import re
import sqlite3


class ParseSqlite:
    def __init__(self, path):
        self.path = path
        self.GET_ALL_HISTORY = "SELECT url FROM moz_places ORDER BY id"

    def get_history_urls(self):
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute(self.GET_ALL_HISTORY)
        all_entries = cursor.fetchall()
        modified_entries = []
        for entry in all_entries:
            match = re.match(r"((http:\/\/)?(https:\/\/)?((\w*[-]*)+(\.)*)+)", entry[0])
            if match:
                modified_entries.append(match[0])
        return modified_entries
