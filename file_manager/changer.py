import os

from file_manager.utils import perm_to_num

class FileChanger:
    def __init__(self, permissions, substitute_of_bad_char, bad_characters):
        self.permissions = permissions
        self.substitute_of_bad_char = substitute_of_bad_char
        self.bad_characters = bad_characters

    def create_good_filename(self, filename):
        for char in self.bad_characters:
            filename = filename.replace(char, self.substitute_of_bad_char)
        return filename

    def process_wrong_named_file(self, filename, ask=True, action=False):
        new_filename = self.create_good_filename(filename)
        if action:
            print("{} renamed to {}".format(filename, new_filename))
            os.rename(filename, new_filename)
            return new_filename
        elif not (ask or action):
            print("Wrong file name {} kept".format(filename))
            return filename
        text = "Filename {} is wrong. Do you want to rename to {}? [Y/n]: "
        choice = input(text.format(filename, new_filename))
        if choice.upper() in ("Y", ""):
            os.rename(filename, new_filename)
            return new_filename
        return filename

    def process_file_permissions(self, filename, perm, ask=True, action=False):
        if action:
            print("Permissions of {} changed to {}".format(filename, self.permissions))
            os.chmod(filename, perm_to_num(self.permissions))
            return True
        elif not (ask or action):
            print("Permissions {} of {} kept".format(perm, filename))
            return False
        text = "Permissions of {} are {}. Do you want to change to {}? [Y/n]: "
        choice = input(text.format(filename, perm, self.permissions))
        if choice.upper() in ("Y", ""):
            os.chmod(filename, perm_to_num(self.permissions))
            return True
        return False