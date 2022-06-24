"""module utils 

Some useful functions for running the program and testing (for examle: create testing directory tree)
"""
import os
import random
import shutil


def file_size(filename):
    """Function to get size of file

    Args:
        filename (str): name of file

    Returns:
        int: size of file
    """
    return os.path.getsize(filename)

def extension_of(filename):
    """Function to get extension of file

    Args:
        filename (str): name of file

    Returns:
        str: extension of file
    """
    return os.path.splitext(filename)[1]

def perm_to_num(perm):
    """Function to convert symbolic permissions (rwxrwxrwx) to numeric permissions in decimal system (511)

    Args:
        perm (str): symbolic permissions

    Returns:
        int: numeric permissions
    """

    # octal system
    perms = {
        "---": '0',
        "--x": '1',
        "-w-": '2',
        "-wx": '3',
        "r--": '4',
        "r-x": '5',
        "rw-": '6',
        "rwx": '7'
    }
    if len(perm) == 10:
        perm = perm[1:]

    user = perm[:-6]
    group = perm[3:-3]
    others = perm[6:]

    numeric = perms[user] + perms[group] + perms[others]
    
    # decimal system
    return int(numeric, 8)

def fill_directory(path, bad_characters, temp_extensions, num_of_files=20):
    """Function to fill directory with testing files

    Args:
        path (str): path to directory
        bad_characters (set(str)): wrong characters in names of files
        temp_extensions (set(str)): temporary extensions of files
        num_of_files (int, optional): Number of generated files. Defaults to 20.
    """
    for i in range(num_of_files):
        try:
            action = "w"
            if i % 4 == 1:
                full_path = path + "test" + str(i) + random.choice(list(temp_extensions))
            elif i % 4 == 2:
                full_path = path + "test" + random.choice(list(bad_characters)) + str(i)
            elif i % 4 == 3:
                full_path = path + "test" + str(i) + "." + chr(random.randint(100, 120))
            else:
                full_path = path + "test" + str(i)

            with open(full_path, action) as f:
                f.write((random.randint(0, 4)) * str(random.randint(0, 4)))
        except Exception as e:
                print(e)

def prepare_files(path, bad_characters, temp_extensions, num_of_copy_dirs=1):
    """Function to prepare testing single-level directory tree

    Args:
        path (str): path to main directory
        bad_characters (set(str)): wrong characters in names of files
        temp_extensions (set(str)): temporary extensions of files
        num_of_copy_dirs (int, optional): Number of copy directories (Y1, Y2...). Defaults to 1.
    """
    for i in range(num_of_copy_dirs + 1):
        dir = "X" if i == 0 else ("Y" + str(i))
        try:
            os.mkdir(path + dir)
        except Exception as e:
            print("During making directory an error occured:", e)
        fill_directory(path + dir + "/", bad_characters, temp_extensions)

def prepare_subfiles(path, bad_characters, temp_extensions, num_of_copy_dirs=1):
    """Function to prepare testing two-level directory tree

    Args:
        path (str): path to main directory
        bad_characters (set(str)): wrong characters in names of files
        temp_extensions (set(str)): temporary extensions of files
        num_of_copy_dirs (int, optional): Number of copy directories (Y1, Y2...). Defaults to 1.
    """
    prepare_files(path, bad_characters, temp_extensions, num_of_copy_dirs)
    for i in range(num_of_copy_dirs + 1):
        for let in ("x", "y", "z"):
            dir = f"X/{let}" if i == 0 else ("Y" + str(i) + f"/{let}")
            try:
                os.mkdir(path + dir)
            except Exception as e:
                print("During making directory an error occured:", e)
            fill_directory(path + dir + "/", bad_characters, temp_extensions)

def get_files(path):
    """Function to get all files' names from main directory and its subdirectories

    Args:
        path (str): path to main directory

    Returns:
        list(str): list of all files' names
    """
    files = os.listdir(path)
    all_files = list()

    for entry in files:
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            all_files = all_files + get_files(full_path)
        else:
            all_files.append(full_path)
                
    return all_files

def get_all_files(path, copy_paths=None):
    """Function to get all files' names from main and copy directories (Y1, Y2,...) and their subdirectories

    Args:
        path (str): path to main directory
        copy_paths (list(str), optional): paths to copy directories. Defaults to None.

    Returns:
        list(str): list of all files' names
    """
    files = get_files(path)

    if copy_paths:
        for copy_path in copy_paths:
            files += get_files(copy_path)

    return files

def move_files_to_main_dir(main_dir_path, copy_paths):
    """Function to move all files from copy directories (Y1, Y2,...) to main directory

    Args:
        main_dir_path (str): path to main directory
        copy_paths (list(str)): paths to copy directories
    """
    for copy_path in copy_paths:
        for filename in get_files(copy_path):
            new_filename = generate_unique_filename(filename, main_dir_path, copy_path)
            shutil.move(filename, new_filename)

def generate_unique_filename(filename, main_dir_path, copy_path):
    """Function to generate unique (in main directory) name of file from copy directory

    Args:
        filename (str): proposed file name
        main_dir_path (str): path to main directory
        copy_path (str): path to copy directory

    Returns:
        str: unique file name
    """
    new_filename = filename.replace(copy_path, main_dir_path)
    if os.path.exists(new_filename):
        i = 1
        name, extension = os.path.splitext(new_filename)
        new_filename = name + "_" + str(i) + extension
        while os.path.exists(new_filename):
            i += 1
            new_filename = str(i).join(new_filename.rsplit(str(i-1), 1))
    return new_filename

def load_configuration(conf_path):
    """Function to load configuration from file

    Args:
        conf_path (str): path to configuration file

    Returns:
        str, set(str), str, set(str): configuration
    """
    with open(conf_path, "r") as f:
        permissions = f.readline().rstrip().replace("permissions: ", "")
        bad_characters = set(f.readline().rstrip().replace("bad-characters: ", "").split(" "))
        substitute = f.readline().rstrip().replace("substitute: ", "")
        temp_extensions = set(f.readline().rstrip().replace("temporary-extensions: ", "").split(" "))
        temp_extensions.add(".tmp")
    return permissions, bad_characters, substitute, temp_extensions
