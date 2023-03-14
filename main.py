from Data import *
import time

if __name__ == "__main__":
    data = Data(blocking_factor=4,alpha=0.5,vn_ratio=0.5)
    print("Interactive (1) or text file input? (2) : ")
    choice = input()
    print()
    if choice == "1":
        while True:
            print("1. Insert record\n2. Reorganize\n3. Print pages\n4. Update record without key\n5. Update record with key\n6. Delete record")
            option = input()
            if option == "1":
                key = int(input("key: "))
                print()
                data.add_record(key)
                data.print_pages()
            elif option == "2":
                data.reorganize()
            elif option == "3":
                data.print_pages()
            elif option == "4":
                key = int(input("key: "))
                print()
                data.update_record(key)
                data.print_pages()
            elif option == "5":
                key = int(input("key: "))
                print()
                new_key = int(input("New key: "))
                print()
                data.update_record_with_key(key, new_key)
                data.print_pages()
            elif option == "6":
                key = int(input("key: "))
                print()
                data.delete_record(key)
                data.print_pages()
    elif choice == "2":
        with open("test_input2.txt", "r") as f:
            lines = f.read()
            for i in range(len(lines)):
                if lines[i] == 'A':
                    x = ""
                    while lines[i+1].isnumeric():
                        x += lines[i+1]
                        i += 1
                    data.add_record(int(x))
                elif lines[i] == 'P':
                    data.print_pages()
                elif lines[i] == 'U':
                    x = ""
                    while lines[i+1].isnumeric():
                        x += lines[i+1]
                        i += 1
                    data.update_record(int(x))
                elif lines[i] == 'D':
                    x = ""
                    while lines[i+1].isnumeric():
                        x += lines[i+1]
                        i += 1
                    data.delete_record(int(x))
                elif lines[i] == 'O':
                    data.reorganize()

    elif choice == "3":
        num_records = [100,200,500,1000,2000]
        for i in range(len(num_records)):
            data_exp = Data(blocking_factor=4, alpha=0.5, vn_ratio=0.5)
            organize_count = 0
            keys = [random.randint(1, 1000) for i in range(num_records[i])]
            start_time = time.time()
            for j in range(num_records[i]):
                data_exp.add_record(keys[j])
            insertion_time = time.time() - start_time
            organize_count = data_exp.organize_count
            # print("Insertion time (num_records = %d): %f seconds" % (num_records[i], insertion_time))
            start_time = time.time()
            for j in range(num_records[i]):
                data_exp.update_record(keys[j])
            update_time = time.time() - start_time

            start_time = time.time()
            for j in range(num_records[i]):
                data_exp.delete_record(keys[j])
                # data_exp.reorganize()
                #reorganize dla fizycznego usuniecia

            delete_time = time.time() - start_time


            with open("experiment.txt", "a") as file:
                file.write(f"num_records: {num_records[i]}\n")
                file.write(f"Insert time: {insertion_time}\n")
                file.write(f"Organize Count: {organize_count}\n")
                file.write(f"Delete time: {delete_time}\n")
                file.write(f"Update time: {update_time}\n")
                file.write("\n")

