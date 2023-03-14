import math
from Record import *
from KeyPage import *

class Data:


    def __init__(self,blocking_factor,alpha,vn_ratio):
        self.blocking_factor = blocking_factor
        self.alpha = alpha
        self.vn_ratio = vn_ratio
        self.organize_count = 0
        self.key_page = []
        self.pages = []
        self.pages_overflow = []
        self.page = []

    def reorganize(self):
        records = []
        updated_records = []
        record = Record(-1, False, None)
        record.first = True
        updated_records.append(record)
        for p in self.pages:
            for r in p:
                if(r.empty == False):
                    records.append(r)
        for p in self.pages_overflow:
            for r in p:
                if (r.empty == False):
                    records.append(r)
        while(len(updated_records) < len(records) + 1):
            for r in records:
                x = r
                if (next((e for e in updated_records if e.key == x.key), None) == None or x.key == -1):
                    updated_records.append(x)
                while(x.overflow_pointer != None):
                    x = x.overflow_pointer
                    if(next((e for e in updated_records if e.key == x.key), None) == None):
                        updated_records.append(x)
        for i in range(len(updated_records)):
            updated_records[i].overflow_pointer = None

        i = 0
        while i < len(updated_records):
            if updated_records[i].to_delete:
                updated_records.pop(i)
            else:
                i += 1
        record.to_delete = True

        self.pages = []
        self.key_page = []
        new_pages = math.ceil(len(updated_records) / 2)
        for i in range(new_pages):
            self.pages.append([])

        iterator = 0

        for list_ in self.pages:
            self.key_page.append(KeyPage(updated_records[0].key, iterator))

            i = 0
            while i < int(self.blocking_factor * self.alpha):
                if (len(updated_records) > 0):
                    list_.append(updated_records[0])
                    updated_records.pop(0)
                    i += 1
                else:
                    break

            for j in range(self.blocking_factor - i): # uzupelnienie strony ppustymi rekordami
                list_.append(Record(0, True, None))

            iterator += 1

        self.pages_overflow = []
        self.page = []
        print("Reorganized")
        self.organize_count += 1

    def add_record(self, key):
            print(f"Inserting {key}")
            new_record = Record(key, False, None)
            if len(self.key_page) > 0:
                page = next(p for p in reversed(self.key_page) if p.key < key).page #pierwsza strona ktora ma klucz mniejszy niz podany
                not_empty_records = [r for r in self.pages[page] if not r.empty]
                if len(not_empty_records) == self.blocking_factor:
                    r = next(r for r in reversed(self.pages[page]) if r.key < key)
                    while r.overflow_pointer is not None:
                        r = r.overflow_pointer
                    r.overflow_pointer = new_record

                    if len(self.pages_overflow) == 0 or len(self.pages_overflow[-1]) == self.blocking_factor:
                        self.pages_overflow.append([new_record])
                    else:
                        self.pages_overflow[-1].append(new_record)
                else:
                    #jest miejsce na stronie zamienia pusty rekord
                    if next(r for r in reversed(self.pages[page]) if not r.empty).key < key: #ostatni niepusty rekord na stronie
                        next(r for r in self.pages[page] if r.empty).key = key  #pierwszy pusty rekord na stronie
                        next(r for r in self.pages[page] if r.empty).overflow_pointer = None
                        next(r for r in self.pages[page] if r.empty).empty = False
                    else:
                        r = next(r for r in reversed(self.pages[page]) if r.key < key and not r.empty) #szuka ostatniego rekordu o kluczu mniejszym niż podany klucz
                        while r.overflow_pointer is not None:
                            r = r.overflow_pointer
                        r.overflow_pointer = new_record
                        if len(self.pages_overflow) == 0 or len(self.pages_overflow[-1]) == self.blocking_factor:
                            self.pages_overflow.append([new_record])
                        else:
                            self.pages_overflow[-1].append(new_record)

            else:
                if len(self.pages_overflow) == 0:
                    self.pages_overflow.append([new_record])
                else:
                    if len(self.pages_overflow[-1]) == self.blocking_factor:
                        self.pages_overflow.append([new_record])
                    elif len(self.pages_overflow[-1]) != self.blocking_factor and self.organize_count == 0:
                        self.pages_overflow[-1].append(new_record)

            if self.should_reorganize() >= self.vn_ratio:
                self.reorganize()




    def print_pages(self):
        print("Main: ")
        for list_ in self.pages:
            for i in range(len(list_)):
                if list_[i].key == -1:
                    print("F", end=" ")
                else:
                    print(list_[i].key if not list_[i].empty else "", end=" ")
                    print(list_[i].data if not list_[i].empty else "E", end=" ")
                    print("D" if list_[i].to_delete else "", end=" ")
                    print("P {}".format(list_[i].overflow_pointer.key) if list_[i].overflow_pointer is not None else "", end=" ")
            print()

        print("Overflow: ")
        for list_ in self.pages_overflow:
            for i in range(len(list_)):
                print(list_[i].key if not list_[i].empty else "", end=" ")
                print(list_[i].data if not list_[i].empty else "E", end=" ")
                print("D" if list_[i].to_delete else "", end=" ")
                print("P {}".format(list_[i].overflow_pointer.key) if list_[i].overflow_pointer is not None else "", end=" ")
            print()

        print("Keypage: ")
        for key in self.key_page:
            if key.key == -1:
                print(f"{self.pages[0][1].key} page: {key.page + 1}")
            else:
                print(f"{key.key} page: {key.page + 1}")

    def update_record(self, key):
        print(f"Updating record with {key}")
        for page in self.pages:
            record = next((e for e in page if e.key == key), None)
            if record is not None:
                record.data=record.generate_record()

        for page in self.pages_overflow:
            record = next((e for e in page if e.key == key), None)
            if record is not None:
                record.data=record.generate_record()

    def update_record_with_key(self, key, new_key):
        print(f"Updating record with {key} to {new_key}")
        for page in self.pages:
            record = next((e for e in page if e.key == key), None)
            if record is not None:
                record.generate_record()

        for page in self.pages_overflow:
            record = next((e for e in page if e.key == key), None)
            if record is not None:
                record.generate_record()

        self.delete_record(key)
        self.add_record(new_key)

    def should_reorganize(self):
        if len(self.pages) == 0:
            return 1
        else:
            return len(self.pages_overflow) / len(self.pages)

    def delete_record(self, key):
        print(f"Deleting {key}")
        for page in self.pages:
            record = next((e for e in page if e.key == key), None)
            if record is not None:
                record.to_delete = True

        for page in self.pages_overflow:
            record = next((e for e in page if e.key == key), None)
            if record is not None:
                record.to_delete = True