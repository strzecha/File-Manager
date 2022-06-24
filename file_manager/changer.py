import os

from file_manager.utils import perm_to_num

class FileChanger:
    """class FileChanger

    Class to change attributes of files (permissions and names)
    """

    def __init__(self, permissions, substitute_of_bad_char, bad_characters):
        """init method

        Args:
            permissions (str): proposed permissions
            substitute_of_bad_char (str): substitute of wrong characters in files' names
            bad_characters (set(str)): wrong characters in files' names
        """
        self.permissions = permissions
        self.substitute_of_bad_char = substitute_of_bad_char
        self.bad_characters = bad_characters

    def generate_correct_filename(self, filename):
        """Method to generate file name without wrong characters

        Args:
            filename (str): (wrong) name of file

        Returns:
            str: correct name of file
        """
        for char in self.bad_characters:
            filename = filename.replace(char, self.substitute_of_bad_char)
        return filename

    def process_wrong_named_file(self, filename, ask=True, action=False):
        """Method to ask (or not) user and process wrong named file 

        Args:
            filename (str): name of file
            ask (bool, optional): whether to ask the user for an action. Defaults to True.
            action (bool, optional): action to prepare (True - keep, False - rename). Defaults to False.

        Returns:
            str: processed name of file
        """
        new_filename = self.generate_correct_filename(filename)
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
        """Method to ask (or not) user and process wrong permissions of file

        Args:
            filename (str): name of file
            perm (str): permissions of file
            ask (bool, optional): whether to ask the user for an action. Defaults to True.
            action (bool, optional): action to prepare (True - keep, False - change permissions). Defaults to False.

        Returns:
            bool: whether the permissions were changed or not
        """
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