import csv,sys,argparse
from impacket import version, ese
from impacket.ese import ESENT_DB

from tools.parse_sqlite import get_unique_urls


class ParseInternetExplorer:
    def __init__(self, path):
        self.path = path

    def get_history_urls(self):
        urls = []
        ese = ESENT_DB(self.path)
        history_containers = []
        container_table = ese.openTable("Containers")
        if container_table is None:
            return
        while True:
            record = ese.getNextRow(container_table)
            if record is None:
                break
            if record["Name"] == "Historyx00" and "History.IE5" in record["Directory"]:
                history_containers.append(record["ContainerId"])

        for container in history_containers:
            history_table = ese.openTable("Container_" + str(container))
            if history_table is None:
                return
            while True:
                record = ese.getNextRow(history_table)
                if record is None:
                    break
                urls.append(record["Url"])

        ese.close()
        return get_unique_urls(urls)