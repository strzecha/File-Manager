import os
import io
import shutil
import stat
import pytest

from file_manager.changer import FileChanger
from file_manager.utils import load_configuration

file_path = "test_changer/"
conf_path = "tests/clean_files_test"

@pytest.fixture(scope="function", autouse=True)
def remove_unnecessary_files():
    for element in os.listdir(os.getcwd()):
        os.remove(element)

@pytest.fixture(scope='module')
def sharedFileChanger():
    perm, bad, sub, _ = load_configuration(conf_path)
    changer = FileChanger(perm, sub, bad)

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

def test_process_file_permissions(sharedFileChanger):
    changer = sharedFileChanger['changer']
    filename = "empty_file"
    open(filename, "x")
    perm = os.stat(filename).st_mode
    perm = stat.filemode(perm)

    assert os.path.exists(filename)
    assert perm == "-rw-rw-r--"
    assert changer.process_file_permissions(filename, perm, False, True)
    assert stat.filemode(os.stat(filename).st_mode) == "-rw-r--r--"

def test_process_file_permissions_user_decision(sharedFileChanger, monkeypatch):
    changer = sharedFileChanger['changer']
    filename = "empty_file"
    open(filename, "x")
    perm = os.stat(filename).st_mode
    perm = stat.filemode(perm)

    assert os.path.exists(filename)

    monkeypatch.setattr('sys.stdin', io.StringIO("N"))
    assert perm == "-rw-rw-r--"
    assert not changer.process_file_permissions(filename, perm)
    assert stat.filemode(os.stat(filename).st_mode) != "-rw-r--r--"

    monkeypatch.setattr('sys.stdin', io.StringIO("Y"))
    assert changer.process_file_permissions(filename, perm)
    assert stat.filemode(os.stat(filename).st_mode) == "-rw-r--r--"

def test_process_wrong_named_file(sharedFileChanger):
    changer = sharedFileChanger['changer']
    filename = "bad,file"
    open(filename, "x")

    assert os.path.exists(filename)
    new_filename = changer.process_wrong_named_file(filename, ask=False, action=True)
    assert not os.path.exists(filename)
    assert os.path.exists(new_filename)
    assert filename.replace(",", changer.substitute_of_bad_char) == new_filename

def test_process_wrong_named_file_user_decision(sharedFileChanger, monkeypatch):
    changer = sharedFileChanger['changer']
    filename = "bad,file"
    open(filename, "x")

    assert os.path.exists(filename)

    monkeypatch.setattr('sys.stdin', io.StringIO("n"))
    new_filename = changer.process_wrong_named_file(filename)
    assert new_filename == filename

    monkeypatch.setattr('sys.stdin', io.StringIO("y"))
    new_filename = changer.process_wrong_named_file(filename)
    assert not os.path.exists(filename)
    assert os.path.exists(new_filename)
    assert filename.replace(",", changer.substitute_of_bad_char) == new_filename