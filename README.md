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
3. `cd ../backend`
4. `python3 -m pip install -r requirements.txt` to install FastAPI & SQLModel dependencies (This must be run every time the container is rebuilt)
5. `python3 -m backend.script.reset_database` to create the database and load in fake data. This can be run as many times as possible to reset the databse.

### Running the Development Server

1. Run `honcho start`
2. Open `http://localhost:4400` to view the application

## Development Concerns

### Backend

To help with backend implementation, you can reference the `count` demo feature. 

#### FastAPI

When creating FastAPI routes, make sure to define the routes in a feature file named corresponding to the feature inside of the `api` directory.
This file should look similar to the example one in `api/count.py`. You will need to import the file in `main.py` and
add it to the `feature_apis` list as well as the tags in the `openapi_tags` list in the `FastAPI()` constructor.

#### SQLModel

Define all SQLModels in the `models` folder in a file named according to the feature. Make sure to add this file to the `__all__` list inside
of the `__init__.py` file in the `models` folder. This will allow it to be imported by default inside of the `create_database` script.

In the future we will support adding fake data inside of the `create_database` script.

## Event Supervisor Command Suite Documentation
### load_teams
#### Description
Loads a local `teams.csv` table into the database. This command will take care of password generation for teams as they are initialized and add them to the csv file. No password overwriting occurs in this script.
#### Command
`python3 -m backend.script.load_teams`
#### Arguments
| Argument | Description |
|----------|----------|
|`file`|File containing updated team information. Upon completing, this file is altered to show the current state of the `team` table in the database|


### reset_database 
#### Description
initializes the database. If a database already exists, it is perminantly overwritten and all data is lost.
#### Command
`python3 -m backend.script.load_teams`
#### Arguments
NA

### reset_unique_words
#### Description
The `unique_word_list` is our current tool for password generation. As more teams are made and more passwords are generated, the word list depletes. This function resets only the word list so that new passwords can be generated.
#### Command
`python3 -m backend.script.load_teams`
#### Arguments
NA
