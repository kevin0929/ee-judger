import glob
import os
import re
import io
import time
import psutil
import subprocess
import pandas as pd

from config import logger
from dependencies import check_all
from tqdm import tqdm


def compile(file_path: str) -> str:
    """compile target program"""

    compile_command = ["gcc", "-o", "program", str(file_path)]
    compile_result = subprocess.Popen(
        compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # wait for compile finish and get err/out message
    compile_result.wait()
    out_msg, err_msg = compile_result.communicate()

    # return result
    if compile_result.returncode == 0:
        return "pass"
    else:
        return err_msg


def sandbox(file_path: str, problem_path: str) -> int:
    """
    execute program avoid running into
    runtime and memory error
    """

    # Parameter config
    time_limit = 1  # second
    memory_limit = 10 * 1024 * 1024  # 10mb
    execution_command = ["./program"]
    this_problem_score = 0

    # Fetch the test data
    input_list = glob.glob(os.path.join(f"{problem_path}/input", "*"))
    output_list = glob.glob(os.path.join(f"{problem_path}/output", "*"))

    # Start judge
    size = len(input_list)
    for idx in range(size):
        # read input and except_output to run and dealwith output result
        input = input_list[idx]
        output = output_list[idx]
        with open(input, "r") as f_in, open(output, "r") as f_out:
            input_data = f_in.read()
            except_output = f_out.read()

        execution_process = subprocess.Popen(
            execution_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        execution_process.stdin.write(input_data.encode())
        execution_process.stdin.close()

        # Get pid number and monitor status for it
        start_time = time.time()
        runpid = execution_process.pid
        monitor = psutil.Process(runpid)

        while execution_process.poll() is None:
            elapsed_time = time.time() - start_time  # Execution time
            mem_info = monitor.memory_info()

            if elapsed_time > time_limit:
                logger.error(f"{file_path} run into TLE.")
                execution_process.kill()
                return 0
            elif mem_info.rss > memory_limit:
                logger.error(f"{file_path} run into RE.")
                execution_process.kill()
                return 0

            time.sleep(0.1)

        # wait for process to terminal
        execution_process.wait()

        output_byte = execution_process.stdout.read()
        output = io.StringIO(output_byte.decode()).read()
        # print(output)

        if output.strip() == except_output.strip():
            this_problem_score += 2
        else:
            this_problem_score += 0

    return this_problem_score


def execution(file_path: str, problem_number: int) -> int:
    """return target problem score"""

    # First step : Compile
    compile_msg = compile(file_path)
    if compile_msg != "pass":
        file_name = file_path.split("\\")[-1]
        logger.error(
            f"The {file_name} can't compile problem {problem_number}, error msg : {compile_msg}"
        )
        return 0

    problem_path = f"test_data/P{problem_number}"

    # Second step : Get result score from sandbox
    this_problem_score = sandbox(file_path, problem_path)

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
            score_dict[int(problem_number)] = score
        except Exception as err:
            logger.error(f"{file_name} has someting wrong, error msg : {err}.")
            score_dict[int(problem_number)] = 0

    return score_dict


if __name__ == "__main__":
    check_all()
    score_df = pd.DataFrame(
        columns=["P1", "P2", "P3", "P4", "P5", "P6"],
        index=["student_id"],
    )
    student_list = glob.glob(os.path.join("code", "*"))

    for student in student_list:
        student_id = student.split("\\")[-1]
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
        print(new_df)
        score_df = pd.concat([score_df, new_df], axis=0)
    score_df.to_csv("final_score.csv")
