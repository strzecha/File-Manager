import os
import random
import shutil


def file_size(file):
    return os.path.getsize(file)

def extension_of(filename):
    return os.path.splitext(filename)[1]

def perm_to_num(perm):
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
    
    return int(numeric, 8)

def fill_directory(path, bad_characters, temp_extensions, num_of_files=20):
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
    for i in range(num_of_copy_dirs + 1):
        dir = "X" if i == 0 else ("Y" + str(i))
        try:
            os.mkdir(path + dir)
        except Exception as e:
            print("During making directory an error occured:", e)
        fill_directory(path + dir + "/", bad_characters, temp_extensions)

def prepare_subfiles(path, bad_characters, temp_extensions, num_of_copy_dirs=1):
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
    files = get_files(path)

    if copy_paths:
        for copy_path in copy_paths:
            files += get_files(copy_path)

    return files

def move_files_to_main_dir(main_dir_path, copy_paths):
    for copy_path in copy_paths:
        for filename in get_files(copy_path):
            new_filename = generate_non_exist_filename(filename, main_dir_path, copy_path)
            shutil.move(filename, new_filename)

def generate_non_exist_filename(filename, main_dir_path, copy_path):
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
    with open(conf_path, "r") as f:
        permissions = f.readline().rstrip().replace("permissions: ", "")
        bad_characters = set(f.readline().rstrip().replace("bad-characters: ", "").split(" "))
        substitute = f.readline().rstrip().replace("substitute: ", "")
        temp_extensions = set(f.readline().rstrip().replace("temporary-extensions: ", "").split(" "))
        temp_extensions.add(".tmp")
    return permissions, bad_characters, substitute, temp_extensions