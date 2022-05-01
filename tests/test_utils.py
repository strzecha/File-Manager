from file_manager.utils import perm_to_num

def test_perm_to_num():
    assert perm_to_num("---------") == 0
    assert perm_to_num("-rwxrwxrwx") == 511
    assert perm_to_num("r---w---x") == 273