from tkinter.filedialog import askdirectory

# Importing required libraries.
from tkinter import Tk
import os
import shutil
import hashlib
from pathlib import Path
import datetime as dt

from sql_model import SQLModel
from secret import username, password

# We don't want the GUI window of
# tkinter to be appearing on our screen
Tk().withdraw()

# Dialog box for selecting a folder.
file_import_path = askdirectory(title="Select a folder to IMPORT files from")
# file_move_path = askdirectory(title="Select a folder to MOVE files to")

sql_model = SQLModel(url='sql.disruptivesoftware.com', user=username, password=password)

# Listing out all the files
# inside our root folder.
print('Crawling filesystem...')
list_of_files = os.walk(file_import_path)

print(f'Querying database for hashes...')
database_hash_set = sql_model.get_file_hashes()
# database_path_set = sql_model.get_file_paths()

# print(f'Found {len(database_hash_set)} hashes in the database\n\n')

# print('WARNING:  This will delete files if they are found in the database.\n')

print(f'SOURCE: {file_import_path}')
# print(f'DESTINATION: {file_move_path}\n\n')

input('Press enter to continue')
'''
Logic:

If the file_hash is in the database.  
    Get the file name from the database.

'''
delete_count = 0
move_count = 0
skip_extensions = ('.txt', '.ini', '.jpg', '.png', '.jpeg', '.gif', '.db')
skip_files = '.DS_Store'

for root, folders, files in list_of_files:
    # Looping on all the files
    for file in files:
        file_path = Path(os.path.join(root, file))

        file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

        if file_hash not in database_hash_set:
            # check for exclusions
            if file.endswith(skip_extensions):
                print(f'Skipping {file_path}')
                continue
            if file in skip_files:
                print(f'Skipping {file_path}')
                continue

            # new_file_path = Path(os.path.join(file_move_path, file))
            # print(f'Moving {file_path}')

            # if new_file_path.exists():
            #     # duplicate filename in destination folder

            #     split_string = file.split('.')
            #     split_string.insert(-1, file_hash[:8])
            #     new_filename = '.'.join(split_string)

            #     print(f'Renaming to: {new_filename}')

            #     new_file_path = Path(os.path.join(file_move_path, f'{new_filename}'))

            # shutil.move(file_path, new_file_path)
            sql_model.add_file(file_hash, str(file_path))
            # database_hash_set.add(file_hash)
            print(f'Added {file_path} to the database')
            move_count += 1
        # else:
        # print(f'Deleting {file_path}')
        # os.remove(file_path)
        # delete_count += 1

# print(f'Deleted {delete_count} files')
print(f'Indexed {move_count} files')
