from typing import List


class Entry:
    def __init__(self, headers: List = [], data: List = []):
        self.id = None
        self.header_names = headers
        self.data = data

    def add_header(self, header_name: str):
        for header in self.header_names:
            if header == header_name:
                raise Exception("Header already exists in inventory")
        self.header_names.append(header_name)

    def add_entry(self, header_name: str, data):
        for i in range(len(header_name)):

            if header_name in self.header_names:
                if self.header_names[i] == header_name:
                    if len(self.data) == i-1:
                        self.data.append(data)
                        break
                    elif i-1 < len(self.data):
                        self.data[i] = data
                        break
            else:
                self.header_names.append(header_name)
                self.data.append(data)
                break


class Inventory:
    def __init__(self):
        self.entries: List[Entry] = []
        self.entry_count = 0

    def add_entry(self, entry: Entry):
        self.entry_count += 1
        entry.id = self.entry_count
        self.entries.append(entry)

    def log(self):
        all_entries = ">>Inventory entry selected-->> "

        index = 0
        for entry in self.entries[0].header_names:
            all_entries += (f"{entry}: {self.entries[0].data[index]}, ")
            index += 1
        print(all_entries)
