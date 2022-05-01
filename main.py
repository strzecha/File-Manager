import argparse

from file_manager.manager import FileManager
from file_manager.utils import get_all_files, move_files_to_main_dir

conf_path = "doc/clean_files"

def main():
    # parsing arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("main_path", type=str)
    parser.add_argument("copy_paths", type=str, nargs="*")
    parser.add_argument("--temp_del", dest="t_del", action="store_true")
    parser.add_argument("--temp_keep", dest="t_keep", action="store_true")
    parser.add_argument("--empty_del", dest="e_del", action="store_true")
    parser.add_argument("--empty_keep", dest="e_keep", action="store_true")
    parser.add_argument("--bad_change", dest="b_change", action="store_true")
    parser.add_argument("--bad_keep", dest="b_keep", action="store_true")
    parser.add_argument("--perm_change", dest="p_change", action="store_true")
    parser.add_argument("--perm_keep", dest="p_keep", action="store_true")
    parser.add_argument("--same_action", dest="s_action", choices=['old', 'new', 'both'])

    args = parser.parse_args()
    path = args.main_path

    ask_empty = not (args.e_del or args.e_keep)
    action_empty = args.e_del
    ask_temp = not (args.t_del or args.t_keep)
    action_temp = args.t_del
    ask_bad = not (args.b_change or args.b_keep)
    action_bad = args.b_change
    ask_perm = not (args.p_change or args.p_keep)
    action_perm = args.p_change
    action_duplicate = args.s_action

    # creating manager
    filenames = get_all_files(path, args.copy_paths)
    manager = FileManager(conf_path, filenames)

    manager.set_parameters(ask_empty=ask_empty, action_empty=action_empty, ask_temporary=ask_temp,
                       action_temporary=action_temp, ask_wrong_name=ask_bad, action_wrong_name=action_bad,
                       ask_permissions=ask_perm, action_permissions=action_perm, action_duplicate=action_duplicate)

    manager.manage_files()

    # moving files to main dir
    move_files_to_main_dir(path, args.copy_paths)

if __name__ == "__main__":
    main()









