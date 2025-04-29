# Event Supervisor Documentation

## Managing the Event Supervisor Graphical User Interface

During the `Setup Environment Variables` step in the [README](/README.md), you were instructed to create a secure administrator username and password. At the home page of the project, switch to the Event Supervisor view and enter the respective login information.

### Scheduling Page

Create sessions and assign teams to sessions.

### Questions Page

Create the test. Each question includes a prompt, starter code, demo cases, test cases, global docs

### Teams Page

Create teams, manage teams, download scores and submissions

## ES File Structure and Question Formatting

#### General File Structure

The general ES file structure should maintained in the following format, and any deviation may cause some backend components to break:

```
es_files/
├─ questions/
│ ├─ q1/
│ │ ├─ prompt.md
│ │ ├─ doc_<title>.md
│ │ ├─ test_cases.py
│ │ ├─ demo_case.py
│ │ ├─ starter.py
│ ├─ q2/
│ ├─ q3/
├─ teams/
│ ├─ unique_words_reset.csv
│ ├─ teams.csv
├─ global_docs/
│ ├─ <title>.md
```

#### `teams` Subdirectory Information

The `teams` subdirectory holds all data for interacting with the Team tables in the database. As of now, there are two important files:

| File                     | Description                                                               |
| ------------------------ | ------------------------------------------------------------------------- |
| `teams.csv`              | File containing a snapshot of the Team table in the database.             |
| `unique_words_reset.csv` | File containing a list of gradeschool level words for password generation |

#### `questions` Subdirectory Information

The `questions` Subdirectory holds information for the test, where it's subdirectories, following the convention q#, represent questions and contain all relevant files.

| File             | Description                                                                             |
| ---------------- | --------------------------------------------------------------------------------------- |
| `prompt.md`      | This Markdown file holds the question body.                                             |
| `doc_<title>.md` | Markdown files with the prefix `doc_` are question specific/supplemental documentation. |
| `test_cases.py`  | This python file is for final submission grading by the ES.                             |
| `demo_cases.py`  | This python file is for validation testing by the students.                             |
| `starter.py`     | This python file is inserted into the text box for the students to work from.           |

#### Writing `demo_cases.py` and `test_cases.py`

Any functionality in the `gradescope_utils` and `unittest` libraries are supported when writing these tests, additional functionality may not be supported.
Specifically in `test_cases.py` it is expected that point values will be assigned to tests using the `@weight(#)` decorator.
If you include the `@weight(#)` decorator in the `demo_cases.py` file, it will be ignored during grading and when running demo tests.

In both files, you will need to import `unittest`, and the function that you are grading's name from the `submission` module. This is how the students submission will be passed to Judge0.

The general template for writing these files are as follows:

```python
"""Demo/test cases for problem #"""

import unittest
from submission import function_name
# To use any of the gradescope utils import them from the package called "decorators"
from decorators import weight

class Test(unittest.TestCase):

    @weight(2) # Only needs to be included in the test_cases.py file
    def test_name_of_test(self):
        self.assertEqual(function_name("input") "expected_output")

    # Note that you can define multiple tests in either file
    @weight(1)
    def test_2(self):
        self.assertEqual(function_name("input"), "expected_output")

```

If you need more information on how to write these tests, please take a look at the `example_test` directory.

## Command Line Scripts

#### `global_docs` Subdirectoy Information

The `global_docs` subdirectory holds all documentation made available regardless of question. All Markdown file in this directory will be made available for reference during test time.

### ES Scripting Suite Documentation

#### `generate_blank_questions`

Generates a template file structure for `the es_files/questions` subdirectory. If questions already exist in the directory, this will generate more questions starting from the largest indexed `q#` found in the subdirectory. Generated questions will be in the format

```
├─ q1/
│ ├─ prompt.md
│ ├─ test_cases.py
│ ├─ demo_case.py
│ ├─ starter.py
```

##### Command

```bash
python3 -m backend.script.generate_blank_questions AMT
```

##### Arguments

| Argument | Description                                     | Default |
| -------- | ----------------------------------------------- | ------- |
| AMT      | The amount of questions to generate. Minimum 1. | 3       |

#### `add_teams`

##### Description

Generates new team entries with unique identifiers based on a specified prefix and saves them to the database and a CSV file. The script takes care of password generation for each team and saves the updated team data back to the specified file. If the CSV file doesn’t exist, it will be created with the appropriate columns.

The script does not update any changes from the file, so anything in the file but not in the database will be reverted similar to the `teams_to_csv` script.

This command follows these rules:

- **New teams** are created with unique names based on the given prefix and are assigned unique passwords.

- **Existing teams** database are shown in the `teams.csv` file.
- The generated team data is saved back to the specified file, ensuring the CSV reflects the current state of the `team` table.

##### Command

```bash
python3 -m backend.script.add_teams PREFIX NUMBER DATE START END [-f, --file=es_files/teams/teams.csv]
```

##### Arguments

| Argument | Flags        | Description                                                                                                                                                               | Default                    |
| -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `PREFIX` | `NA`         | Alphabetic prefix for team names. Each new team name will start with this prefix, followed by a unique number.                                                            | `NA`                       |
| `NUMBER` | `NA`         | Number of new teams to create. This must be an integer.                                                                                                                   | `NA`                       |
| `DATE`   | `NA`         | Date for team activities in the format `mm/dd/yyyy`.                                                                                                                      | `NA`                       |
| `START`  | `NA`         | Start time for team activities in `HH:MM` format (24h time), on the specified date.                                                                                       | `NA`                       |
| `END`    | `NA`         | End time for team activities in `HH:MM` format (24h time), on the specified date.                                                                                         | `NA`                       |
| `FILE`   | `-f, --file` | Path to the CSV file where the updated team information will be saved. If the file does not exist, it will be created with default columns. Must have a `.csv` extension. | `es_files/teams/teams.csv` |

---

#### `load_teams`

##### Description

Loads a local `teams.csv` table into the database. This command will take care of password generation for teams as they are initialized and add them to the csv file. No password overwriting occurs in this script.

This command is _safe_... meaning it follows these rules:
Where a team is identified by it's team number...

1. Any team in the database but NOT in the file will be added to the file
2. Any team in the file but NOT in the database will be added to the database
3. Any team in both the file and database will update the database to the file's fields (if there are changes)

##### Command

```bash
python3 -m backend.script.load_teams [-f, --file=es_files/teams/teams.csv]
```

##### Arguments

| Argument | Flag         | Description                                                                                                                                    | Default                    |
| -------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `FILE`   | `-f, --FILE` | File containing updated team information. Upon completing, this file is altered to show the current state of the `team` table in the database. | `es_files/teams/teams.csv` |

#### `grade_submissions`

##### Description

This script is the one stop shop for calculating grades for students. The following will happen for each team defined in the database and for each question defined in the `es_files/questions` directory:

- The question's `test_cases.py` file will be run with that teams submission defined in `es_files/submissions`.
- The output of each test (or the single statement that they did not submit, or a `test_cases.py` file was not configued) will be added to a row in the outputted `scored_tests.csv`
- The total score over all tests for each team will appear in `final_scores.csv`

Both of these files, `scored_tests.csv` and `final_scores.csv` are by default found in the `es_files/teams` directory.

This command does not take in any arguments. Successive runs will overwrite current files.

##### Command

```
python3 -m backend.script.grade_submissions
```

#### `teams_to_csv`

##### Description

Updates or generates a teams.csv file containing the current state of the database.

This command is **NOT safe**... meaning any changes in the teams.csv file will be deleted!

##### Command

```bash
python3 -m backend.script.teams_to_csv [-f, --file=es_files/teams/teams.csv]
```

##### Arguments

| Argument | Flags        | Description                                                                                                                                                      | Default                    |
| -------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `FILE`   | `-f, --file` | File to be filled with team table information. Upon completing, this file is altered or generated to show the current state of the `team` table in the database. | `es_files/teams/teams.csv` |

#### `teams_to_db`

##### Description

Updates the teams table in the database to match the teams.csv file provided.

This command is **NOT safe**... meaning any changes and deletions in the teams.csv will be permanent!

it follows these rules:
Where a team is identified by it's team number...

1. Any team in the database but NOT in the file will be **DELETED** from the database
2. Any team in the file but NOT in the database will be **ADDED** to the database
3. Any team present in both will be **UPDATED** according to the file's specifications

##### Command

```bash
python3 -m backend.script.teams_to_db [-f, --file=es_files/teams/teams.csv]
```

##### Arguments

| Argument | Flags        | Description                                                                                                                      | Default                    |
| -------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| `FILE`   | `-f, --file` | File containing updated team information. Upon successful completion, the database will be updated to the file's specifications. | `es_files/teams/teams.csv` |

#### `reset_unique_words`

##### Description

The `unique_word_list` is our current tool for password generation. As more teams are made and more passwords are generated, the word list depletes. This function resets only the word list so that new passwords can be generated.

##### Command

```bash
python3 -m backend.script.reset_unique_words
```

##### Arguments

`NA`

#### `reset_teams`

##### Description

**Will permenantly delete ALL DATA in the team table of the database.**

##### Command

```bash
python3 -m backend.script.reset_teams
```

##### Arguments

`NA`
