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
usage: quiz.py [-h] [-s SOLUTION_FILE] [--select SELECT] [question_dir ...]

positional arguments:
  question_dir

options:
  -h, --help            show this help message and exit
  -s SOLUTION_FILE, --solution-file SOLUTION_FILE
  --select SELECT
```

By default quiz.py considers the current working directory the question directory and treats all present files as questions.

## Requirements

* PySimpleGUI

## License

The quiz.py program is licensed under the terms of the GNU General Public License
version 3. A Copy of the license is included in the `LICENSE` file.

The sound [Wrong.mp3](https://freesound.org/people/LittleRainySeasons/sounds/335906/) licensed under the terms of the Creative Commons 0 License.
The sound [Correct.mp3](https://freesound.org/people/milton./sounds/77103/) by Milton Paredes is licensed under the terms of the Attribution NonCommercial 3.0 License.
