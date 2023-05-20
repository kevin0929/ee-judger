import re
from pathlib import Path

from config import logger


def check_folder_name(path: Path) -> None:
    """
    To get the name of every student's folder,
    and remove superfluous words except student id.
    """

    # To set regex rule
    student_id_regex = re.compile(r"\d{10}")
    for folder in path.glob("*"):
        folder_name = folder.name
        try:
            student_id = student_id_regex.search(folder_name).group()
            # If there are superfluous words in name, remove it
            if folder_name != student_id:
                folder.rename(path / student_id)
        except Exception as err:
            logger.error(f"{student_id} format wrong, error message : {err}")

        # To check the files name which in folder
        check_file_name(folder)


def check_file_name(path: Path) -> None:
    """
    Check P is upper and file type is .c
    if file type is .cpp, change it to .c,
    and if file type is other, delete it
    """

    # To set regex rule
    file_name_regex = re.compile(r"\d{10}_P\d")
    for file in path.glob("*"):
        # Deal with path problem
        basename, typename = file.stem, file.suffix

        # Check P is upper
        basename = basename.replace("p", "P")

        # Check file type
        if typename == ".exe":
            file.unlink()
        else:
            new_file_name = file_name_regex.match(basename).group()
            file.rename(path / f"{new_file_name}.c")


def check_all() -> None:
    """check all"""
    check_folder_name(Path("code"))
