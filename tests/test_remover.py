import os
import shutil
import io
import pytest

from file_manager.remover import FileRemover

file_path = "test_remover/"

@pytest.fixture(scope="function", autouse=True)
def remove_unnecessary_files():
    for element in os.listdir(os.getcwd()):
        os.remove(element)

@pytest.fixture(scope='module', autouse=True)
def check_dir():
    # create directory with tests
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.mkdir(file_path)
    os.chdir(file_path)
    yield

    # remove directory with tests
    os.chdir("..")
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

def test_process_empty_file():
    remover = FileRemover()
    filename = "empty_file"
    open(filename, "x")

    assert os.path.exists(filename)

    assert not remover.process_empty_file(filename, ask=False, action=False)
    assert os.path.exists(filename)

    assert remover.process_empty_file(filename, ask=False, action=True)
    assert not os.path.exists(filename)

def test_process_empty_file_user_decision(monkeypatch):
    remover = FileRemover()
    filename = "empty_file"
    open(filename, "x")

    monkeypatch.setattr('sys.stdin', io.StringIO("N"))
    assert os.path.exists(filename)
    assert not remover.process_empty_file(filename)

    monkeypatch.setattr('sys.stdin', io.StringIO("Y"))
    assert remover.process_empty_file(filename)
    assert not os.path.exists(filename)

def test_process_temporary_file():
    remover = FileRemover()
    filename = "temporary_file.temp"
    open(filename, "x")

    assert os.path.exists(filename)
    assert remover.process_temporary_file(filename, ask=False, action=True)
    assert not os.path.exists(filename)

    filename = "temporary_file~"
    open(filename, "x")

    assert os.path.exists(filename)
    assert remover.process_temporary_file(filename, ask=False, action=True)
    assert not os.path.exists(filename)

def test_process_temporary_file_user_decision(monkeypatch):
    remover = FileRemover()
    filename = "temporary_file.temp"
    open(filename, "x")

    monkeypatch.setattr('sys.stdin', io.StringIO("N"))
    assert os.path.exists(filename)
    assert not remover.process_temporary_file(filename)
    assert os.path.exists(filename)

    monkeypatch.setattr('sys.stdin', io.StringIO("Y"))
    assert os.path.exists(filename)
    assert remover.process_temporary_file(filename)
    assert not os.path.exists(filename)

    filename = "temporary_file~"
    open(filename, "x")

    monkeypatch.setattr('sys.stdin', io.StringIO("N"))
    assert os.path.exists(filename)
    assert not remover.process_temporary_file(filename)
    assert os.path.exists(filename)

    monkeypatch.setattr('sys.stdin', io.StringIO("Y"))
    assert os.path.exists(filename)
    assert remover.process_temporary_file(filename)
    assert not os.path.exists(filename)

def test_process_group_of_filenames_by_size():
    remover = FileRemover()
    filename1 = "empty_file1"
    open(filename1, "x")
    filename2 = "empty_file2"
    open(filename2, "x")
    filename3 = "empty_file3"
    open(filename3, "x")

    assert os.path.exists(filename1)
    assert os.path.exists(filename2)
    assert os.path.exists(filename3)

    filenames = [filename1, filename2, filename3]
    remover.process_group_of_filenames_by_size(filenames, "old")
    
    assert not os.path.exists(filename1)
    assert not os.path.exists(filename2)
    assert os.path.exists(filename3)
