import os
import stat

from file_manager.utils import load_configuration, extension_of, file_size
from file_manager.remover import FileRemover
from file_manager.changer import FileChanger


class FileManager:
    """class FileManager

    Class to manage files
    """
    def __init__(self, conf_path, filenames=[]):
        """init method

        Args:
            conf_path (str): path to configuration file
            filenames (list, optional): list of files' names to manage. Defaults to [].
        """
        (attr, bad, sub, temp) = load_configuration(conf_path)
        self.attributes = attr
        self.bad_characters = bad
        self.substitute = sub
        self.temp_extensions = temp
        self.filenames = filenames

        self.ask_empty = False
        self.action_empty = True
        self.ask_temporary = False
        self.action_temporary = True
        self.ask_wrong_name = False
        self.action_wrong_name = True
        self.ask_permissions = False
        self.action_permissions = True
        self.action_duplicate = 'old'

        self.remover = FileRemover()
        self.changer = FileChanger(attr, sub, bad)

    def get_filenames(self):
        """Getter of filenames

        Returns:
            list(str): files' names
        """
        return self.filenames

    def set_filenames(self, filenames):
        """Setter of filenames

        Args:
            filenames (list(str)): list of files' names
        """
        self.filenames = filenames

    def get_temp_extensions(self):
        """Getter of temp_extensions

        Returns:
            set(str): set of temporary extensions
        """
        return self.temp_extensions

    def get_bad_characters(self):
        """Getter of bad_characters

        Returns:
            set(str): set of wrong characters in files' names
        """
        return self.bad_characters   

    def set_parameters(self, ask_empty=False, action_empty=True, ask_temporary=False,
                       action_temporary=True, ask_wrong_name=False, action_wrong_name=True,
                       ask_permissions=False, action_permissions=True, action_duplicate='old'):
        """Setter of managing parameters

        Args:
            ask_empty (bool, optional): wheter ask to remove empty files. Defaults to False.
            action_empty (bool, optional): default action about empty files (True - keep, False - remove). Defaults to True.
            ask_temporary (bool, optional): wheter ask to remove temporary files. Defaults to False.
            action_temporary (bool, optional): default action about temporary files (True - keep, False - remove). Defaults to True.
            ask_wrong_name (bool, optional): wheter ask to rename wrong named files. Defaults to False.
            action_wrong_name (bool, optional): default action about wrong named files (True - keep, False - rename). Defaults to True.
            ask_permissions (bool, optional): wheter ask to change wrong permissions of files. Defaults to False.
            action_permissions (bool, optional): default action about wrong permissions of files (True - keep, False - change). Defaults to True.
            action_duplicate (str, optional): default action about duplicated files ("new" - remove newer file, "old" - remove older files, "none" - keep both). Defaults to 'old'.
        """
        self.ask_empty = ask_empty
        self.action_empty = action_empty
        self.ask_temporary = ask_temporary
        self.action_temporary = action_temporary
        self.ask_wrong_name = ask_wrong_name
        self.action_wrong_name = action_wrong_name
        self.ask_permissions = ask_permissions
        self.action_permissions = action_permissions
        self.action_duplicate = action_duplicate

    def remove_empty_files(self):
        """Method to remove all empty files (with asking user or not)
        """
        new_filenames = self.filenames[:]
        for filename in self.filenames:
            if file_size(filename) == 0:
                if self.remover.process_empty_file(filename, self.ask_empty, self.action_empty):
                    new_filenames.remove(filename)
        self.filenames = new_filenames

    def rename_wrong_named_files(self):
        """Method to rename all wrong named files (with asking user or not)
        """
        new_filenames = list()
        for filename in self.filenames:
            if len(self.bad_characters.intersection(filename)) > 0:
                filename = self.changer.process_wrong_named_file(filename, self.ask_wrong_name, self.action_wrong_name)
            new_filenames.append(filename)
        self.filenames = new_filenames

    def remove_temporary_files(self):
        """Method to remove all temporary files (with asking user or not)
        """
        new_filenames = self.get_filenames()[:]
        for filename in self.filenames:
            if extension_of(filename) in self.temp_extensions or filename[-1] == "~":
                if self.remover.process_temporary_file(filename, self.ask_temporary, self.action_temporary):
                    new_filenames.remove(filename)
        self.filenames = new_filenames

    def change_bad_files_permissions(self):
        """Method to change all wrong permissions of files (with asking user or not)
        """
        for filename in self.filenames:
            perm = os.stat(filename).st_mode
            perm = stat.filemode(perm)

            if perm != self.attributes:
                self.changer.process_file_permissions(filename, perm, self.ask_permissions, self.action_permissions)

    def sort_and_group_filenames_by_size(self):
        """Method to sort files by size

        Yields:
            list(str): group of names of files with the same size
        """
        # sort by size
        self.filenames = sorted(self.filenames, key=lambda x: os.path.getsize(x))

        files_same_size = []
        for i in range(len(self.filenames)):
            filename = self.filenames[i]

            if len(files_same_size) == 0:
                files_same_size.append(filename)
            elif file_size(filename) == file_size(files_same_size[-1]):
                files_same_size.append(filename)
            else:
                yield files_same_size
                files_same_size = [filename]


            if i == len(self.filenames) - 1:
                yield files_same_size

    def remove_duplicate_files(self):
        """Method to removeduplicated files (with asking user or not)
        """
        removed_filenames = list()

        for group in self.sort_and_group_filenames_by_size():
            filenames = self.remover.process_group_of_filenames_by_size(group, self.action_duplicate)
            removed_filenames.extend(filenames)

        self.filenames = [filename for filename in self.filenames if filename not in removed_filenames]

    def manage_files(self):
        """Method to manage all files
        """
        self.remove_empty_files()
        self.remove_temporary_files()
        self.remove_duplicate_files()

        self.change_bad_files_permissions()
        self.rename_wrong_named_files()
    
