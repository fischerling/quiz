# simple interactive quiz

The script was designed for prompting simple Questions from the german Känguru
math contest. It displays questions from picture or PDF files and uses a simple
GUI to prompt for the correct solution.

## Preparations

Before using quiz.py one must arrange a pool of question files.
The simplest way to specify the solution for each question is to create a
solutions file called `solutions.csv` in the same directory as the questions.
The solutions file must provide the fields `question,solution`.

## Usage

```
usage: quiz.py [-h] [-s SOLUTION_FILE] [--select SELECT] [--question-match QUESTION_MATCH]
               [--answers [ANSWERS ...]]
               [question_dir ...]

positional arguments:
  question_dir          directories containing questions

options:
  -h, --help            show this help message and exit
  -s SOLUTION_FILE, --solution-file SOLUTION_FILE
                        file containing the solutions
  --select SELECT       selector string to identify a subset of solutions
  --question-match QUESTION_MATCH
                        match question files names
  --answers [ANSWERS ...]
                        match question files names
```

By default quiz.py considers the current working directory the question directory and treats all present files as questions.

## Requirements

* python >= 3.11
* PySimpleGUI
* playsound
* psutil

The requirements can be installed in virtual environment using [`pipenv`](https://pipenv.pypa.io/) or using the `requirements.txt` file

## License

The quiz.py program is licensed under the terms of the GNU General Public License
version 3. A Copy of the license is included in the `LICENSE` file.

The sound [Wrong.mp3](https://freesound.org/people/LittleRainySeasons/sounds/335906/) licensed under the terms of the Creative Commons 0 License.
The sound [Correct.mp3](https://freesound.org/people/milton./sounds/77103/) by Milton Paredes is licensed under the terms of the Attribution NonCommercial 3.0 License.
