import re
import os
import glob

from config import logger


def check_folder_name(path: str) -> None:
    """
    To get the name of every student's folder,
    and remove superfluous words except student id.
    """

    folder_path = os.path.join(path, "*")
    folder_list = glob.glob(folder_path)

    # To set regex rule
    student_id_regex = re.compile(r"\d{10}")
    for folder in folder_list:
        folder_name = folder.split("\\")[-1]
        try:
            student_id = student_id_regex.search(folder_name).group()
            # If there are superfluous words in name, remove it
            if folder_name != student_id:
                os.rename(f"{path}/{folder_name}", f"{path}/{student_id}")
        except Exception as err:
            logger.error(f"{student_id} format wrong, error message : {err}")

        # To check the files name which in folder
        check_file_name(folder)


def check_file_name(path: str) -> None:
    """
    Check P is upper and file type is .c
    if file type is .cpp, change it to .c,
    and if file type is other, delete it
    """

    file_path = os.path.join(path, "*")
    file_list = glob.glob(file_path)

    # To set regex rule
    file_name_regex = re.compile(r"\d{10}_P\d")
    for file in file_list:
        # Deal with path problem
        file_name = file.split("\\")[-1]
        basename, typename = os.path.splitext(file_name)

        # Check P is upper
        basename = basename.replace("p", "P")

        # Check file type
        if typename == ".exe":
            os.remove(file)
        else:
            new_file_name = file_name_regex.match(basename).group()
            os.rename(file, f"{path}\\{new_file_name}.c")


def check_all() -> None:
    """check all"""
    check_folder_name("code")
