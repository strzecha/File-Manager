import os
import filecmp
from itertools import combinations

class FileRemover:
    """class FileRemover

    Class to remove empty, temporary or duplicated files
    """
    def remove_file(self, filename, output=True):
        """Method to remove file and print message

        Args:
            filename (str): name of file
            output (bool or str, optional): result (True of False) of removing or name of removed file. Defaults to True.

        Returns:
            bool or str: result (True of False) of removing or name of removed file
        """
        print("{} removed".format(filename))
        os.remove(filename)
        return output

    def keep_file(self, filename, output=False):
        """Method to print message about keeping file

        Args:
            filename (str): name of file
            output (bool, optional): result of removing file. Defaults to Faldr.

        Returns:
            bool: result of removing file
        """
        print("{} kept".format(filename))
        return output

    def ask_to_remove(self, filename, ask, action):
        """Method to ask to remove file and perform chosen operation

        Args:
            filename (str): name of file
            ask (bool): whether to ask the user for an action
            action (bool): action to prepare (True - keep, False - remove)

        Returns:
            bool: result of removing
        """
        if action:
            return self.remove_file(filename)
        elif not (ask or action):
            return self.keep_file(filename)

        choice = input("Remove? [Y/n]: ")
        if choice.upper() in ("Y", ""):
            return self.remove_file(filename)

        return False

    def process_empty_file(self, filename, ask=True, action=False):
        """Method to process empty file

        Args:
            filename (str): name of file
            ask (bool): whether to ask the user for an action
            action (bool): action to prepare (True - keep, False - remove)

        Returns:
            bool: result of removing
        """
        print("File {} is empty".format(filename))
        return self.ask_to_remove(filename, ask, action)

    def process_temporary_file(self, filename, ask=True, action=False):
        """Method to process temporary file

        Args:
            filename (str): name of file
            ask (bool): whether to ask the user for an action
            action (bool): action to prepare (True - keep, False - remove)

        Returns:
            bool: result of removing
        """
        print("File {} is temporary".format(filename))
        return self.ask_to_remove(filename, ask, action)

    def process_duplicate_files(self, filename1, filename2, action=None):
        """Method to process duplicated files

        Args:
            filename1 (str): name of first file
            filename2 (str): name of second file
            action (str): action to prepare ("new" - remove newer file, "old" - remove older file, "none" - keep both files)

        Returns:
            str: name of removed file
        """
        (filename1, filename2) = sorted([filename1, filename2], key=lambda x: os.path.getctime(x))

        print("{} (old) and {} (new) are identical.".format(filename1, filename2))
        if action == "new":
            return self.remove_file(filename2, filename2)
        elif action == "old":
            return self.remove_file(filename1, filename1)
        elif action == "none":
            print("{} (old) and {} (new) kept".format(filename1, filename2))
            return None

        choice = input("Which remove? Old, New or nonE? [O/n/e]: ".format(filename1))
        if choice.upper() in ("O", ""):
            return self.remove_file(filename1, filename1)
        elif choice.upper() == "N":
            return self.remove_file(filename2, filename2)
        return None

    def process_group_of_filenames_by_size(self, filenames, action="none"):
        """Method to process group of filenames to find and remove duplicated files

        Args:
            filenames (list(str)): list of files' names
            action (str, optional): action to prepare ("new" - remove newer file, "old" - remove older file, "none" - keep both files). Defaults to "none".

        Returns:
            list(str): list of names of removed files
        """
        removed_filenames = list()
        for pair in combinations(filenames, 2):
            if os.path.exists(pair[0]) and os.path.exists(pair[1]):
                if filecmp.cmp(pair[0], pair[1], False):
                    removed_filename = self.process_duplicate_files(*pair, action)
                    removed_filenames.append(removed_filename)
        return removed_filenames
