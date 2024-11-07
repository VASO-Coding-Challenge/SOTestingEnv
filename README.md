# Science Olympiad Testing Environment

This project aims to create a web-based coding platform specifically tailored for Science Olympiad programming events.

For more information visit our [COMP523 E-Team Website here](https://tarheels.live/eteam/).

## Get Programming

### Running the DevContainer

1. Install Docker Desktop and the DevContainers extension in VSCode
2. Clone the repo into VSCode and open it
3. Press `Ctrl+Shift+P` on windows (`Cmd+Shift+P`?? on mac) to open the command pallet and run `Dev Containers: Build and Reopen in Container` (In the future to open you can just use `Dev Containers: Reopen in Container`)
4. Grab some water while the container builds

### Installing Dependencies

Run the following commands:

1. `cd frontend`
2. `npm install` to install React dependencies
3. `python3 -m backend.script.reset_database` to create the database and load in fake data. This can be run as many times as possible to reset the databse.

### Setup Environment Variables

1. `cd backend`
2. Generate a random secret key via: `openssl rand -hex 32`
3. Create a new file called `.env.development` with the following contents:

```
SECRET_KEY=<Your Generated Secret Key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running the Development Server

1. Run `honcho start`
2. Open `http://localhost:4400` to view the application

## Development Concerns

### Frontend

#### React Router

If you would like to create a new page and add it to the app itself. You would need to create the file, and if you have intellisense for react snippets, you can run "tsrafce" to spin up a component/page.

Now move to App.tsx. Import the page from the component you had just created. and add the following underneath the Routes tag:

```jsx
<Route path="[PATH THAT SHOWS IN THE URL]" element ={<[YOUR PAGE] />} />
```

Then you're all set to continue development!

### Backend

To help with backend implementation, you can reference the `count` demo feature.

#### FastAPI

When creating FastAPI routes, make sure to define the routes in a feature file named corresponding to the feature inside of the `api` directory.
This file should look similar to the example one in `api/count.py`. You will need to import the file in `main.py` and
add it to the `feature_apis` list as well as the tags in the `openapi_tags` list in the `FastAPI()` constructor.

#### Requiring Authentication

##### Basic Auth

To require a user to be logged in to access a route, and get their associated Team table, add this argument to the route:

```python
from .auth import authed_team
...
def get_foo(
team: Team = Depends(authed_team)
):
```

##### Timed Access

To require a user to be authenticated, in their scheduled test time (between the start and end values in their team table),
and retreieve their `Team` object, use the `active_test` function found in `/api/auth.py`. Adding it to a route is just as simple
as basic auth:

```python
from .auth import active_test
...
def testing_concerns(
    team: Team = Depends(active_test)
):
```

This function will return a `401` error if the team is not authenticated (there is no valid JWT token), and a `403` error if the 
current time is not during their test time.

#### SQLModel

Define all SQLModels in the `models` folder in a file named according to the feature. Make sure to add this file to the `__all__` list inside
of the `__init__.py` file in the `models` folder. This will allow it to be imported by default inside of the `create_database` script.

In the future we will support adding fake data inside of the `create_database` script.

##### reset_database

###### Description

initializes the database. If a database already exists, it is perminantly overwritten and all data is lost.
Also loads in fake data.

###### Command

```bash
python3 -m backend.script.reset_database
```

###### Arguments

NA

## Event Supervisor Documentation

### ES File Structure and Question formatting

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

#### `global_docs` Subdirectoy Information

The `global_docs` subdirectory holds all documentation made available regardless of question. All Markdown file in this directory will be made available for reference during test time.

### ES Scripting Suite Documentation

#### `create_team_table`

##### Description

Generates new team entries with unique identifiers based on a specified prefix and saves them to the database and a CSV file. The script takes care of password generation for each team and saves the updated team data back to the specified file. If the CSV file doesn’t exist, it will be created with the appropriate columns.

The script does not update any changes from the file, so anything in the file but not in the database will be reverted similar to the `teams_to_csv` script.

This command follows these rules:

- **New teams** are created with unique names based on the given prefix and are assigned unique passwords.

- **Existing teams** database are shown in the `teams.csv` file.
- The generated team data is saved back to the specified file, ensuring the CSV reflects the current state of the `team` table.

##### Command

```bash
python3 -m backend.script.create_team_table <prefix> <number_of_teams> <date> <start_time> <end_time> <file_path>
```

##### Arguments

| Argument          | Description                                                                                                                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prefix`          | Alphabetic prefix for team names. Each new team name will start with this prefix, followed by a unique number.                                                                                                |
| `number_of_teams` | Number of new teams to create. This must be an integer.                                                                                                                                                       |
| `date`            | Date for team activities in the format `mm/dd/yyyy`.                                                                                                                                                          |
| `start_time`      | Start time for team activities in `HH:MM` format (24h time), on the specified date.                                                                                                                           |
| `end_time`        | End time for team activities in `HH:MM` format (24h time), on the specified date.                                                                                                                             |
| `file_path`       | Path to the CSV file where the updated team information will be saved. If the file does not exist, it will be created with default columns. Must have a `.csv` extension. DEFAULT: `es_files/teams/teams.csv` |

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

`python3 -m backend.script.load_teams <file_path>`

##### Arguments

| Argument    | Description                                                                                                                                                                        |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path` | File containing updated team information. Upon completing, this file is altered to show the current state of the `team` table in the database. Default: `es_files/teams/teams.csv` |

#### `teams_to_csv`

##### Description

Updates or generates a teams.csv file containing the current state of the database.

This command is **NOT safe**... meaning any changes in the teams.csv file will be deleted!

##### Command

```bash
python3 -m backend.script.teams_to_csv <file_path>
```

##### Arguments

| Argument    | Description                                                                                                                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path` | OPTIONAL. File to be filled with team table information. Upon completing, this file is altered or generated to show the current state of the `team` table in the database. Default: `es_files/teams/teams.csv` |

#### `teams_to_database`

##### Description

Updates the teams table in the database to match the teams.csv file provided.

This command is **NOT safe**... meaning any changes and deletions in the teams.csv will be perminant!

it follows these rules:
Where a team is identified by it's team number...

1. Any team in the database but NOT in the file will be **DELETED** from the database
2. Any team in the file but NOT in the database will be **ADDED** to the database
3. Any team present in both will be **UPDATED** according the file's specifications

##### Command

```bash
python3 -m backend.script.teams_to_database <file_path>
```

##### Arguments

| Argument    | Description                                                                                                                      |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `file_path` | File containing updated team information. Upon successful completion, the database will be updated to the file's specifications. |

#### `reset_unique_words`

##### Description

The `unique_word_list` is our current tool for password generation. As more teams are made and more passwords are generated, the word list depletes. This function resets only the word list so that new passwords can be generated.

##### Command

```bash
python3 -m backend.script.reset_unique_words
```

##### Arguments

NA

#### `reset_teams`

##### Description

**Will permenantly delete ALL DATA in the team table of the database.**

##### Command

```bash
python3 -m backend.script.reset_teams
```

##### Arguments

NA
