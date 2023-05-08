import glob
import os
import io
import subprocess

from config import logger
from dependencies import check_all


def compile(file_path: str) -> bool:
    """ compile target program """

    compile_command = ["gcc", "-o", "test", str(file_path)]
    compile_result = subprocess.run(
        compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # return result
    if compile_result.returncode == 0:
        return True
    else:
        return False


def execution(file_path: str, problem: int) -> int:
    """ return target problem score """

    # First step : compile
    if not compile(file_path):
        file_name = file_path.split("\\")[-1]
        logger.error(f"The {file_name} can not compile problem {problem}")
        return 0

    this_problem_score = 0
    execution_command = ["./test"]
    problem_path = f"test_data/P{problem}"
    input_list = glob.glob(os.path.join(f"{problem_path}/input", "*"))
    output_list = glob.glob(os.path.join(f"{problem_path}/output", "*"))
    # start judge
    length = len(input_list)
    for idx in range(length):
        # read input and except_output to run and dealwith output result
        with open(input_list[idx], "r") as f_in, \
             open(output_list[idx], "r") as f_out:
            input_data = f_in.read()
            except_output = f_out.read()
        # print(f"input : {input_data}, output : {except_output}")
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


def get_all_score(folder_path: str, problem_number: int) -> dict:
    """ traverse all problem for one student """

    score_dict = {idx: None for idx in range(1, problem_number + 1)}
    file_list = glob.glob(os.path.join(f"code/{folder_path}", "*"))
    for idx in range(0, problem_number):
        score = execution(file_list[idx], idx + 1)
        score_dict[idx + 1] = score

    return score_dict


if __name__ == "__main__":
    check_all()
    score_dict = get_all_score("4111064130", 6)
    print(score_dict)
