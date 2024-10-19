# %%
# Count the number of files in a folder and its subfolders

import os

def count_files_in_folder(folder_path):
    total_files = 0
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)
    return total_files

def main():
    folder_path = input("Enter the path to the folder: ")
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    
    total_files = count_files_in_folder(folder_path)
    print(f"Total number of files in '{folder_path}' and its subfolders: {total_files}")

if __name__ == '__main__':
    main()


