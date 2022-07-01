import sqlite3


class DbService:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.db.cursor()

        # SQL
        self.CREATE_TABLE = """
                create table urls
                (
                    url      VARCHAR
                        constraint urls_pk
                            primary key,
                    category VARCHAR,
                    UNIQUE(url)
                );
        """
        self.CHECK_TABLE_EXISTS = """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='urls' """
        self.INSERT_ENTRY = """
            insert or ignore into urls (url, category) values (?, ?);
        """
        self.UPDATE_ENTRY = """
            update urls set category = ? where url = ?
        """
        self.SELECT_ALL_ENTRIES = """SELECT rowid, * FROM urls"""
        self.SELECT_ENTRIES_BY_LIMIT = """SELECT rowid, * FROM urls limit ?, ?"""
        self.GET_ENTRY_COUNT = """SELECT COUNT(*) FROM urls"""

        # Add table init
        self.cursor.execute(self.CHECK_TABLE_EXISTS)
        if self.cursor.fetchone()[0] != 1:
            self.cursor.execute(self.CREATE_TABLE)
        self.db.commit()

    def write_entry(self, urls, categories):
        for index in range(len(urls)):
            if categories[index] != "":
                self.cursor.execute(self.UPDATE_ENTRY, (categories[index], urls[index]))
        self.db.commit()

    def write_entry_with_no_category(self, urls):
        for index in range(len(urls)):
            self.cursor.execute(self.INSERT_ENTRY, (urls[index], ""))
        self.db.commit()

    def get_entries(self, start=None, limit=None):
        if start is None and limit is None:
            self.cursor.execute(self.SELECT_ALL_ENTRIES)
        else:
            self.cursor.execute(self.SELECT_ENTRIES_BY_LIMIT, (start, limit))
        return self.cursor.fetchall()

    def get_entries_count(self):
        return self.cursor.execute(self.GET_ENTRY_COUNT).fetchone()[0]
