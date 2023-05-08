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
    file_name_regex = r"\d{10}_P\d.c"
    for file in file_list:
        # Deal with path problem
        file = file.replace("\\", "/")
        file_name = file.split("/")[-1]
        print(file_name)

        # Check file type
        file_type = file_name.split(".")[-1]
        if file_type == "c":
            continue
        elif file_type == "cpp":
            new_file_name = f"{file_name}.c"
            os.rename(file, f"{path}\\{new_file_name}")
        else:
            os.remove(file)
            continue

        # Check P is upper
        if file_name.find("p") != -1:
            new_file_name = file_name.replace("p", "P")
            os.rename(f"{path}/{file_name}", f"{path}/{new_file_name}")

        # Check .c instead .c.c
        if file_name.find(".c.c") != -1:
            new_file_name = f"{file_name}.c"
            os.rename(f"{path}/{file_name}", f"{path}/{new_file_name}")

        # Final check the file name is right
        if not re.match(file_name_regex, file_name):
            os.remove(file)
            logger.error(f"{file_name} format wrong!")


def check_all() -> None:
    """check all"""
    check_folder_name("code")
