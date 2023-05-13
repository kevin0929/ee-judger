import glob
import os
import re
import io
import subprocess
import pandas as pd

from config import logger
from dependencies import check_all
from tqdm import tqdm


def compile(file_path: str) -> bool:
    """compile target program"""

    compile_command = ["gcc", "-o", "test", str(file_path)]
    compile_result = subprocess.run(
        compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # return result
    if compile_result.returncode == 0:
        return True
    else:
        return False


def execution(file_path: str, problem_number: int) -> int:
    """return target problem score"""

    # First step : compile
    if not compile(file_path):
        file_name = file_path.split("\\")[-1]
        logger.error(f"The {file_name} can't compile problem {problem_number}")
        return 0

    this_problem_score = 0
    execution_command = ["./test"]
    problem_path = f"test_data/P{problem_number}"
    input_list = glob.glob(os.path.join(f"{problem_path}/input", "*"))
    output_list = glob.glob(os.path.join(f"{problem_path}/output", "*"))
    # start judge
    length = len(input_list)
    for idx in range(length):
        # read input and except_output to run and dealwith output result
        input = input_list[idx]
        output = output_list[idx]
        with open(input, "r") as f_in, open(output, "r") as f_out:
            input_data = f_in.read()
            except_output = f_out.read()

        execution_result = subprocess.run(
            execution_command,
            input=input_data.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output_byte = execution_result.stdout.decode()
        output = io.StringIO(output_byte).read()

        # compare output and except_output
        if output.strip() == except_output.strip():
            this_problem_score += 2
        else:
            continue

    return this_problem_score


def get_all_score(folder_path: str, problem_total_number: int) -> dict:
    """traverse all problem for one student"""

    score_dict = {idx: 0 for idx in range(1, problem_total_number + 1)}
    file_list = glob.glob(os.path.join(folder_path, "*"))

    for file in file_list:
        # Fetch problem number
        file_name = file.split("\\")[-1]
        match = re.search(r"P(\d+)\.c", file_name)
        problem_number = match.group(1)

        try:
            score = execution(file, problem_number)
            score_dict[problem_number] = score
        except Exception as err:
            logger.error(f"{file_name} has someting wrong, error msg : {err}.")
            score_dict[problem_number] = 0

    return score_dict


if __name__ == "__main__":
    check_all()
    score_df = pd.DataFrame(
        columns=["P1", "P2", "P3", "P4", "P5", "P6"],
        index=["0"],
    )
    student_list = glob.glob(os.path.join("code", "*"))

    for student in tqdm(student_list):
        student_id = student.split("\\")[-1]
        print(student_id)
        student_dict = get_all_score(student, 6)
        new_df = pd.DataFrame(
            {
                "P1": student_dict[1],
                "P2": student_dict[2],
                "P3": student_dict[3],
                "P4": student_dict[4],
                "P5": student_dict[5],
                "P6": student_dict[6],
            },
            index=[student_id],
        )
        score_df = pd.concat([score_df, new_df], axis=0)
    score_df.to_csv("final_score.csv")
