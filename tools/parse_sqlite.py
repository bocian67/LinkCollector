import re
import sqlite3


def get_unique_urls(entries):
    # Get unique url bases
    unique_entries = []
    for entry in entries:
        match = re.match(r"((http:\/\/)?(https:\/\/)?((\w*[-]*)+(\.)*)+)", entry[0])
        if match:
            unique_entries.append(match[0])
    return unique_entries


def get_history_urls(path, sql_get_history):
    # Get history from path using specified query
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(sql_get_history)
    all_entries = cursor.fetchall()
    return get_unique_urls(all_entries)


class ParseFirefox:
    # Define history parameter for Firefox
    def __init__(self, path):
        self.path = path
        self.GET_ALL_HISTORY = "SELECT url FROM moz_places ORDER BY id"

    def get_history_urls(self):
        return get_history_urls(self.path, self.GET_ALL_HISTORY)


# Is also used to parse Edge
class ParseChrome:
    # Define history parameter for Chrome (and Edge)
    def __init__(self, path):
        self.path = path
        self.GET_ALL_HISTORY = "SELECT url FROM urls ORDER BY id"

    def get_history_urls(self):
        return get_history_urls(self.path, self.GET_ALL_HISTORY)

