import os
import stat
import shutil
import pytest

from file_manager.manager import FileManager
from file_manager.utils import file_size, load_configuration

file_path = "test_manager/"
conf_path = "tests/clean_files_test"

@pytest.fixture(scope="function", autouse=True)
def remove_unnecessary_files():
    # remove all created files after each test
    for element in os.listdir(os.getcwd()):
        os.remove(element)

@pytest.fixture(scope="module")
def configuration():
    (perm, bad, sub, temp) = load_configuration(conf_path)
    return locals()

@pytest.fixture(scope='module', autouse=True)
def check_dir():
    # create directory with tests
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.mkdir(file_path)
    os.chdir(file_path)
    global conf_path
    conf_path = "../" + conf_path
    yield

    # remove directory with tests
    os.chdir("..")
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

def test_manager(configuration):
    manager = FileManager(conf_path, ["test"])

    assert manager.get_bad_characters() == configuration['bad']
    assert manager.get_temp_extensions() == configuration['temp']
    assert manager.get_filenames() == ["test"]

def test_remove_empty_files():
    filenames = list()
    for i in range(5):
        filename = "empty_file" + str(i)
        open(filename, "x")
        filenames.append(filename)
        assert os.path.exists(filename)

    non_empty_filename = "non_empty_file"
    with open(non_empty_filename, "w") as f:
        f.write("something")
    filenames.insert(3, non_empty_filename)

    manager = FileManager(conf_path, filenames)
    manager.remove_empty_files()

    assert len(manager.get_filenames()) == 1
    assert manager.get_filenames()[0] == non_empty_filename
    
    for filename in filenames:
        if filename == non_empty_filename:
            assert os.path.exists(filename)
        else:
            assert not os.path.exists(filename)

def test_remove_temporary_files():
    filename1 = "temp_file.tmp"
    open(filename1, "x")
    filename2 = "non_temp_file"
    open(filename2, "x")
    filename3 = "temp_file.temp"
    open(filename3, "x")
    filename4 = "temp_file~"
    open(filename4, "x")

    assert os.path.exists(filename1)
    assert os.path.exists(filename2)
    assert os.path.exists(filename3)
    assert os.path.exists(filename4)

    filenames = [filename1, filename2, filename3, filename4]
    manager = FileManager(conf_path, filenames)
    manager.remove_temporary_files()

    assert len(manager.get_filenames()) == 1
    assert manager.get_filenames()[0] == filename2
    assert not os.path.exists(filename1)
    assert os.path.exists(filename2)
    assert not os.path.exists(filename3)
    assert not os.path.exists(filename4)

def test_rename_wrong_named_files(configuration):
    bad_chars = list(configuration['bad'])
    bad_chars = [bad_chars[i % len(bad_chars)] for i in range(3)]

    filename1 = f"wrongfile{bad_chars[0]}1"
    open(filename1, "x")
    filename2 = f"wrongfile{bad_chars[1]}2"
    open(filename2, "x")
    filename3 = f"wrongfile{bad_chars[2]}3"
    open(filename3, "x")
    filename4 = "goodfile"
    open(filename4, "x")

    filenames = [filename1, filename2, filename3, filename4]

    for filename in filenames:
        assert os.path.exists(filename)

    manager = FileManager(conf_path, filenames)
    manager.rename_wrong_named_files()

    assert len(manager.get_filenames()) == 4
    for filename, old_filename, char in zip(manager.get_filenames(), filenames, bad_chars):
        assert filename == old_filename.replace(char, configuration['sub'])

def test_change_bad_files_permissions(configuration):
    filenames = list()
    for i in range(5):
        filename = "file" + str(i)
        filenames.append(filename)
        open(filename, "x")

    manager = FileManager(conf_path, filenames)

    manager.change_bad_files_permissions()

    for filename in manager.get_filenames():
        assert stat.filemode(os.stat(filename).st_mode) == configuration['perm']

def test_remove_duplicate_files():
    filenames = list()
    for i in range(3):
        for j in range(3):
            filename = "file{}_{}".format(str(i), str(j))
            filenames.append(filename)
            with open(filename, "w") as file:
                file.write(str(j) * j)

    manager = FileManager(conf_path, filenames)

    manager.remove_duplicate_files()

    assert len(manager.get_filenames()) == 3
    assert os.path.exists(filenames[-1])
    assert os.path.exists(filenames[-3])
    assert not os.path.exists(filenames[0])
    assert not os.path.exists(filenames[4])

def test_manage_files(configuration):
    (permissions, bad_characters, substitute, temp_extensions) = configuration.values()

    filenames = list()
    for i in range(5):
        filename = "empty_file" + str(i)
        filenames.append(filename)
        open(filename, 'x')

        filename = "temporary_file" + str(i) + list(temp_extensions)[i % len(temp_extensions)]
        filenames.append(filename)
        open(filename, 'x')

        filename = "duplicate_file" + str(i)
        filenames.append(filename)
        with open(filename, 'w') as file:
            file.write("duplicate content")

        filename = "wrong_file" + list(bad_characters)[i % len(bad_characters)] + str(i)
        filenames.append(filename)
        with open(filename, "w") as file:
            file.write("test " * (i+1))

        
    manager = FileManager(conf_path, filenames)

    manager.manage_files()

    assert len(manager.get_filenames()) == 6 # 1 duplicate + 5 wrong
    assert len(os.listdir(os.getcwd())) == len(manager.get_filenames())

    for filename in manager.get_filenames():
        # only good permissions
        assert stat.filemode(os.stat(filename).st_mode) == permissions
        # no bad characters
        assert len(bad_characters.intersection(set(filename))) == 0 
        # no empty files
        assert file_size(filename) > 0
        # no temporary files
        assert os.path.splitext(filename)[1] not in temp_extensions 

def test_manage_files2():
    (permissions, bad_characters, substitute, temp_extensions) = load_configuration(conf_path)

    filenames = list()
    for i in range(5):
        filename = "empty_file" + str(i)
        filenames.append(filename)
        open(filename, 'x')

        filename = "temporary_file" + str(i) + list(temp_extensions)[i % len(temp_extensions)]
        filenames.append(filename)
        open(filename, 'x')

        filename = "duplicate_file" + str(i)
        filenames.append(filename)
        with open(filename, 'w') as file:
            file.write("duplicate content")

        filename = "wrong_file" + list(bad_characters)[i % len(bad_characters)] + str(i)
        filenames.append(filename)
        with open(filename, "w") as file:
            file.write("test " * (i+1))

        
    manager = FileManager(conf_path, filenames)
    manager.set_parameters(action_empty=False, action_duplicate='none')

    manager.manage_files()

    assert len(manager.get_filenames()) == 15 # 5 empty + 5 duplicate + 5 wrong
    assert len(os.listdir(os.getcwd())) == len(manager.get_filenames())

    for filename in manager.get_filenames():
        # only good permissions
        assert stat.filemode(os.stat(filename).st_mode) == permissions
        # no bad characters
        assert len(bad_characters.intersection(set(filename))) == 0 
        # no temporary files
        assert os.path.splitext(filename)[1] not in temp_extensions 

def test_manage_files3():
    (permissions, bad_characters, substitute, temp_extensions) = load_configuration(conf_path)

    filenames = list()
    for i in range(5):
        filename = "empty_file" + str(i)
        filenames.append(filename)
        open(filename, 'x')

        filename = "temporary_file" + str(i) + list(temp_extensions)[i % len(temp_extensions)]
        filenames.append(filename)
        open(filename, 'x')

        filename = "duplicate_file" + str(i)
        filenames.append(filename)
        with open(filename, 'w') as file:
            file.write("duplicate content")

        filename = "wrong_file" + list(bad_characters)[i % len(bad_characters)] + str(i)
        filenames.append(filename)
        with open(filename, "w") as file:
            file.write("test " * (i+1))

        
    manager = FileManager(conf_path, filenames)
    manager.set_parameters(action_temporary=False, action_empty=False)

    manager.manage_files()

    assert len(manager.get_filenames()) == 7 # 1 empty/temporary duplicate + 1 duplicate + 5 wrong
    assert len(os.listdir(os.getcwd())) == len(manager.get_filenames())

    for filename in manager.get_filenames():
        # only good permissions
        assert stat.filemode(os.stat(filename).st_mode) == permissions
        # no bad characters
        assert len(bad_characters.intersection(set(filename))) == 0 
