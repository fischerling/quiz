#!/usr/bin/env python3
# Copyright 2023 Florian Fischer
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
"""simple interactive quiz with variable question pool"""

import argparse
import csv
from pathlib import Path
import random
import platform
import tomllib
import subprocess
import sys

import PySimpleGUI as sg
import psutil

WRONG_SOUND = Path(__file__).parent / 'Wrong.mp3'
CORRECT_SOUND = Path(__file__).parent / 'Correct.mp3'

if platform.system() != 'windows':
    SHOW_QUESTION_CMD = 'xdg-open'
    PLAY_SOUND_CMD = 'mpv'
else:
    SHOW_QUESTION_CMD = 'cmd.exe /c start'
    PLAY_SOUND_CMD = 'vlc.exe --intf=dummy --dummy-quiet'


def err(msg: str, status=1):
    """Print the error message to stderr and exit with status"""
    print(msg)
    sys.exit(status)


def play_sound(sound: Path):
    """Play a sound file"""
    subprocess.run(f'{PLAY_SOUND_CMD} {sound}'.split(),
                   check=True,
                   stderr=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL)


def terminate_subprocesses():
    """Terminate all started subprocesses"""
    procs = psutil.Process().children(recursive=True)
    for proc in procs:
        proc.terminate()
    _, alive = psutil.wait_procs(procs)
    for proc in alive:
        proc.kill()


def possible_questions(question_dirs: list[Path]) -> list[Path]:
    """return all file in the question directories"""
    questions = []
    ignored_file_names = [Path(__file__).name, 'solutions']
    for question_dir in question_dirs:
        if not question_dir.is_dir():
            err(f'question directory {question_dir} is not a directory')

        questions.extend([
            p for p in question_dir.iterdir() if p.is_file()
            if p.name not in ignored_file_names
        ])

    return questions


def read_solutions_from_toml(solution_path: Path,
                             selector='') -> dict[str, str]:
    """return solutions from a toml solutions file

    Nested tables can be selected using the selector.
    """

    with open(solution_path, 'rb') as solution_file:
        solution_data = tomllib.load(solution_file)

    if selector:
        for key in selector.split('.'):
            solution_data = solution_data[key]

    return solution_data


def read_solutions_from_csv(path: Path) -> dict[str, str]:
    """return solutions from a csv solutions file"""
    with open(path, 'r', encoding='utf-8') as solution_file:
        csvreader = csv.reader(solution_file, delimiter=',')
        solution_data = list(csvreader)

    # Skip obtional header
    if solution_data[0] == ['question', 'solution']:
        solution_data = solution_data[1:]

    return dict(solution_data)


def load_solutions(question_dirs: list[Path],
                   solution_files: list[Path],
                   selector='') -> dict[str, str]:
    """return solutions for the loaded questions

    solutions must be either in a solutions file per question directory or in
    a single solutions file.
    Solution files must be toml or csv files. 
    Nested tables can be selected using the selector.
    """
    solutions = {}

    if len(question_dirs) == len(solution_files):
        q_s_mapping = list(zip(question_dirs, solution_files))
    elif len(solution_files) == 1:
        q_s_mapping = [(qd, solution_files[0]) for qd in question_dirs]
    else:
        err('question and solution file mismatch')

    for question_dir, solution_path in q_s_mapping:
        if not solution_path.is_file():
            err(f'solution file {solution_path} does not exist')

        if solution_path.suffix == '.toml':
            solutions_from_file = read_solutions_from_toml(solution_path,
                                                           selector=selector)
        elif solution_path.suffix == '.csv':
            solutions_from_file = read_solutions_from_csv(solution_path)
        else:
            err(f'Unsupported solution file format: {solution_path.suffix}')

        flattened_solutions = {
            f'{question_dir / k}': str(v)
            for k, v in solutions_from_file.items()
        }
        solutions.update(flattened_solutions)

    return solutions


def show_question(question: Path) -> subprocess.Popen:
    """show the question in an external programm and return the process"""
    cmd = f'{SHOW_QUESTION_CMD} {question}'.split()
    return subprocess.Popen(cmd)


def color_button(layout, text: str, color: str):
    """Colorize the button containing the text"""
    for button in layout:
        if button.get_text() == text:
            button.update(button_color=color)
            break


def prompt_solution(solution: str, prompts=None):
    """prompt for the solution"""
    if prompts is None:
        prompts = ['A', 'B', 'C', 'D', 'E']

    layout = [[sg.Button(c) for c in prompts]]
    window = sg.Window('', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        try:
            event, _ = window.read()
        except KeyboardInterrupt:
            sys.exit(0)

        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == solution:
            break

        color_button(layout[0], event, '#FF0000')
        play_sound(WRONG_SOUND)

    color_button(layout[0], event, '#00FF00')
    play_sound(CORRECT_SOUND)

    window.read()
    window.close()


def main():
    """main entry point of the quiz"""

    parser = argparse.ArgumentParser()
    parser.add_argument('question_dir',
                        nargs='*',
                        help='directories containing questions')
    parser.add_argument('-s',
                        '--solution-file',
                        help='file containing the solutions')
    parser.add_argument(
        '--select', help='selector string to identify a subset of solutions')
    args = parser.parse_args()

    question_dirs = [Path(p) for p in args.question_dir or ['.']]
    questions = possible_questions(question_dirs)

    solution_files = []
    if args.solution_file:
        solution_files.append(Path(args.solution_file))
    else:
        solution_files.extend([p / 'solutions.csv' for p in question_dirs])

    solutions = load_solutions(question_dirs, solution_files, args.select)

    solved = []
    while questions:
        next_question = random.choice(questions)
        solution = solutions[f'{next_question.parent / next_question.stem}']
        print(f'{next_question}: {solution}', end='')

        show_question(next_question)
        prompt_solution(solution)
        terminate_subprocesses()

        solved.append(next_question)
        questions.remove(next_question)
        print(' Done.')

    print(f'Solved: {solved}')


if __name__ == '__main__':
    main()
