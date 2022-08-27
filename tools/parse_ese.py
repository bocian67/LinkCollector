import re

import pyesedb


def get_unique_urls(entries):
    # Method to get unique url bases
    unique_entries = []
    for entry in entries:
        match = re.match(r"((http:\/\/)?(https:\/\/)?((\w*[-]*)+(\.)*)+)", entry)
        if match:
            unique_entries.append(match[0])
    return unique_entries


class ParseInternetExplorer:
    def __init__(self, path):
        self.path = path

    def get_history_urls(self):
        # Parse Internet Explorer ESE database
        file = open(self.path, "rb")
        esedb_file = pyesedb.file()
        esedb_file.open_file_object(file)
        containers_table = esedb_file.get_table_by_name("Containers")
        web_history_tables = []
        urls = []
        # Get container with history
        for record in range(0, containers_table.get_number_of_records() - 1):
            container_record = containers_table.get_record(record)
            container_id = container_record.get_value_data_as_integer(0)
            container_name = container_record.get_value_data_as_string(8)
            container_directory = container_record.get_value_data_as_string(10)
            if container_name == "History" and "History.IE5" in container_directory:
                web_history_tables += [container_id]

        for record in web_history_tables:
            # Get urls from history containers
            web_history_table = esedb_file.get_table_by_name("Container_" + str(record))
            for j in range(0, web_history_table.get_number_of_records() - 1):
                web_history_record = web_history_table.get_record(j)
                url_string = web_history_record.get_value_data_as_string(17)
                splitted_url = str(url_string).split("@")
                url = splitted_url[-1]
                urls.append(url)
        esedb_file.close()
        file.close()
        # Get unique urls bases and return
        urls = get_unique_urls(urls)
        return urls
