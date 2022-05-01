import os
import stat

from file_manager.utils import load_configuration, extension_of, file_size
from file_manager.remover import FileRemover
from file_manager.changer import FileChanger


class FileManager:
    def __init__(self, conf_path, filenames=[]):
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
        return self.filenames

    def set_filenames(self, filenames):
        self.filenames = filenames

    def get_temp_extensions(self):
        return self.temp_extensions

    def get_bad_characters(self):
        return self.bad_characters   

    def set_parameters(self, ask_empty=False, action_empty=True, ask_temporary=False,
                       action_temporary=True, ask_wrong_name=False, action_wrong_name=True,
                       ask_permissions=False, action_permissions=True, action_duplicate='old'):
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
        new_filenames = self.filenames[:]
        for filename in self.filenames:
            if file_size(filename) == 0:
                if self.remover.process_empty_file(filename, self.ask_empty, self.action_empty):
                    new_filenames.remove(filename)
        self.filenames = new_filenames

    def rename_wrong_named_files(self):
        new_filenames = list()
        for filename in self.filenames:
            if len(self.bad_characters.intersection(filename)) > 0:
                filename = self.changer.process_wrong_named_file(filename, self.ask_wrong_name, self.action_wrong_name)
            new_filenames.append(filename)
        self.filenames = new_filenames

    def remove_temporary_files(self):
        new_filenames = self.get_filenames()[:]
        for filename in self.filenames:
            if extension_of(filename) in self.temp_extensions or filename[-1] == "~":
                if self.remover.process_temporary_file(filename, self.ask_temporary, self.action_temporary):
                    new_filenames.remove(filename)
        self.filenames = new_filenames

    def change_bad_files_permissions(self):
        for filename in self.filenames:
            perm = os.stat(filename).st_mode
            perm = stat.filemode(perm)

            if perm != self.attributes:
                self.changer.process_file_permissions(filename, perm, self.ask_permissions, self.action_permissions)

    def sort_and_group_filenames_by_size(self):
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
        removed_filenames = list()

        for group in self.sort_and_group_filenames_by_size():
            filenames = self.remover.process_group_of_filenames_by_size(group, self.action_duplicate)
            removed_filenames.extend(filenames)

        self.filenames = [filename for filename in self.filenames if filename not in removed_filenames]

    def manage_files(self):
        self.remove_empty_files()
        self.remove_temporary_files()
        self.remove_duplicate_files()

        self.change_bad_files_permissions()
        self.rename_wrong_named_files()
    
