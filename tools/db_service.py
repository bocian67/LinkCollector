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
        self.BY_LIMIT = """ limit ?, ?"""
        self.CATEGORY = """ category=?"""
        self.NOT_CATEGORY = """ NOT category=?"""
        self.NAME = """ url LIKE ?"""
        self.AND = """ AND"""
        self.OR = """ OR"""
        self.WHERE = """ WHERE"""
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
            self.cursor.execute(self.SELECT_ALL_ENTRIES + self.BY_LIMIT, (start, limit))
        return self.cursor.fetchall()

    def get_entries_with_filter(self, name_filter=None, include_category_filter=None, exclude_category_filter=None, start=None, limit=None):
        sql = self.SELECT_ALL_ENTRIES
        add_and = False
        has_where = False
        values = ()
        if name_filter is not None:
            sql += self.WHERE
            has_where = True
            sql += self.NAME
            values += ('%' + name_filter + '%',)
            add_and = True
        if include_category_filter is not None:
            if add_and:
                sql += self.AND
            if not has_where:
                sql += self.WHERE
                has_where = True
            if isinstance(include_category_filter, list):
                add_or = False
                for category_filter in include_category_filter:
                    if add_or:
                        sql += self.OR
                    sql += self.CATEGORY
                    values += (category_filter,)
                    add_or = True
            else:
                sql += self.CATEGORY
                values += (include_category_filter,)
            add_and = True
        if exclude_category_filter is not None:
            if add_and:
                sql += self.AND
            if not has_where:
                sql += self.WHERE
                has_where = True
            if isinstance(exclude_category_filter, list):
                add_or = False
                for category_filter in exclude_category_filter:
                    if add_or:
                        sql += self.OR
                    sql += self.NOT_CATEGORY
                    values += (category_filter,)
                    add_or = True
            else:
                sql += self.NOT_CATEGORY
                values += (exclude_category_filter,)
            add_and = True
        if start is not None and limit is not None:
            sql += self.BY_LIMIT
            values += (start, limit)
        self.cursor.execute(sql, values)
        return self.cursor.fetchall()

    def get_entries_count(self, name_filter=None, include_category_filter=None, exclude_category_filter=None):
        sql = self.GET_ENTRY_COUNT
        add_and = False
        has_where = False
        values = ()
        if name_filter is not None:
            sql += self.WHERE
            has_where = True
            sql += self.NAME
            values += ('%' + name_filter + '%',)
            add_and = True
        if include_category_filter is not None:
            if add_and:
                sql += self.AND
            if not has_where:
                sql += self.WHERE
                has_where = True
            sql += self.CATEGORY
            values += (include_category_filter,)
            add_and = True
        if exclude_category_filter is not None:
            if add_and:
                sql += self.AND
            if not has_where:
                sql += self.WHERE
                has_where = True
            sql += self.NOT_CATEGORY
            values += (exclude_category_filter,)
            add_and = True
        self.cursor.execute(sql, values)
        return self.cursor.fetchone()[0]