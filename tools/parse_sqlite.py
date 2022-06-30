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
        object_id = 0
        for entry in all_entries:
            match = re.match(r"((http:\/\/)?(https:\/\/)?(\w*\.)?(\w*\.)+(\w*)+)", entry[0])
            if match:
                url_object = {"url": match[0], "id": object_id, "category": ""}
                if not any(element["url"] == match[0] for element in modified_entries):
                    modified_entries.append(url_object)
                    object_id += 1
        return modified_entries
