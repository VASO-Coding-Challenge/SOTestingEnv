# Science Olympiad Testing Environment

This project aims to create a web-based coding platform specifically tailored for Science Olympiad programming events.

For more information visit our [COMP523 E-Team Website here](https://tarheels.live/eteam/).

## Get Programming

### Download the Repo

1. Install Docker Desktop, VSCode, and the DevContainer VSCode extension
2. Clone the repo into VSCode and open it

### Setup [Judge0](https://github.com/judge0/judge0)

*Note: This is to be completed *outside\* the devcontainer

1. Download the [judge0 config file](https://github.com/judge0/judge0/blob/ffd7a48cc6da86d6ac155ef10dbd67d02736070b/judge0.conf)
2. Place the file in the `judge0` directory
3. Visit [this website](https://www.random.org/passwords/?num=1&len=32&format=plain&rnd=new) to generate a random password
4. Use this password as the `REDIS_PASSWORD` variable in the `judge0.conf` file.
5. Visit [this website again](https://www.random.org/passwords/?num=1&len=32&format=plain&rnd=new) to generate a new random password
6. Use this new password as the `POSTGRES_PASSWORD` variable in the `judge0.conf` file.

> Note: the following judge0 setup steps must be run every time you wish to run the development server

7. Make sure your current working directory is set to `judge0` (`cd judge0`)
8. Run `bash start.sh` to launch the judge0 server
9. The first time you run this: put some pizza in the oven

> When you wish to exit development don't forget to stop judge0, either via `docker-compose down` inside the `judge0` directory (make sure you are outside the devcontainer!) or stopping the container in Docker Desktop.

**IMPORTANT NOTE FOR OS X USERS (And maybe others)**
Depending on your docker version, the Judge0 workers may not run properly.

To fix the issue, you need modify the Docker Group settings...

1. You can also locate the `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier) at:

- Mac: `~/Library/Group\ Containers/group.com.docker/settings-store.json`
- Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
- Linux: `~/.docker/desktop/settings-store.json`

Open the path in your terminal (Mac OS X zsh example)

```zsh
open ~/Library/Group\ Containers/group.com.docker/settings-store.json
```

2. Find `"DeprecatedCgroupv1"`,
   - If it exists, set to `true`
   - If it does not, append `"DeprecatedCgroupv1": true,` to the json.

### Running the DevContainer

1. Navigate back to the repo in VSCode
2. Press `Ctrl+Shift+P` on windows (`Cmd+Shift+P` on mac) to open the command pallet and run `Dev Containers: Build and Reopen in Container` (In the future to open you can just use `Dev Containers: Reopen in Container`)
3. Grab some water while the container builds

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

#### Uploading the HTML Python Documentation

1. To upload the HTML Python Documentation, visit this link:
   https://docs.python.org/3/download.html

2. Download the zip folder located at the intersection of the
   "HTML" row and "Packed as .zip" column.

3. Extract that Zip folder and drag it into the project's "public" folder.

4. Rename the folder to "python_docs"

5. Make sure to add the newly added documentation's path in the .gitignore file.

You're all set to have added Python Documentation for the project.

##### For Future Reference, Placing more documentation

Current Python Version for documentation: 3.13

To add in a new set of documentation, i.e. Java, JavaScript...

1. Make sure to grab the html documentation for the language.

2. Extract the zip(if needed), and place into the project's "public" folder.

3. Make sure to rename the tile of the folder to something like python_docs
   or {PROGRAMMING_LANGUAGE}\_docs

4. Find the index.html file for your set of documentation.

5. Navigate to SubmissionWidget.tsx and find the section where the docsTab
   is set to "global".

6. Underneath the pre-existing Python list tag, create the following
   JSX Link tag nested inside of an HTML list tag (Similar to the Python one previously placed):

```jsx
<li>
  <Link
    to="YOUR_FOLDER_NAME'S_PATH_TO_INDEX.HTML"
    target="__blank"
    rel="noopener noreferrer"
    className="text-blue-500 hover:text-blue-300"
  >
    'YOUR_PROGRAMMING_LANGUAGE' Documentation
  </Link>
</li>
```

7. Make sure to add the newly added documentation's path in the .gitignore file.

8. Refresh the project and you'll see your link placed inside the Global Docs tab under Docs!

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

#### `generate_blank_questions`

Generates a template file structure for `the es_files/questions` subdirectory. If questions already exist in the directory, this will generate more questions starting from the largest indexed `q#` found in the subdirectory. Generated questions will be in the format

```
├─ q1/
│ ├─ prompt.md
│ ├─ test_cases.py
│ ├─ demo_case.py
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

This command is **NOT safe**... meaning any changes and deletions in the teams.csv will be perminant!

it follows these rules:
Where a team is identified by it's team number...

1. Any team in the database but NOT in the file will be **DELETED** from the database
2. Any team in the file but NOT in the database will be **ADDED** to the database
3. Any team present in both will be **UPDATED** according the file's specifications

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
