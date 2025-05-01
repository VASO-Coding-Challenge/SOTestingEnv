# Science Olympiad Testing Environment

This project aims to create a web-based coding platform specifically tailored for Science Olympiad programming events.

Two COMP523 groups worked on this project. For more information visit our websites:

- [Fall 2024 COMP523 E-Team](https://tarheels.live/eteam/)
- [Spring 2025 COMP523 C-Team](https://tarheels.live/comp523teamc2025/)

## Get Programming

> Note: These instructions are for setting up the development environment. Please see [here](/docs/deploy.md) for exam day setup.

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

7. Run `pushd judge0 ; ./start.sh ; popd` to launch the judge0 server. The first time you run this: put some pizza in the oven.

> When you wish to exit development don't forget to stop judge0, either via `pushd judge0 ; docker-compose down ; popd` (make sure you are outside the devcontainer!) or stopping the container in Docker Desktop.

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

Run these commands to install the React dependencies:

`pushd frontend ; npm install ; popd`

### Setup Environment Variables

1. `cd backend`
2. Generate a random secret key via: `openssl rand -hex 32`
3. Generate a secure password via: `openssl rand -hex 6`, or come up with your own
4. Create a new file called `.env.development` with the following contents:

```
SECRET_KEY=<Your Generated Secret Key>
ACCESS_TOKEN_EXPIRE_MINUTES=90
ES_USERNAME=<Create a Username>
ES_PASSWORD=<Choose a Secure Password>
```

5. `cd ..`

### Download the HTML Python Documentation

1. To download the HTML Python Documentation, visit this link:
   https://docs.python.org/3/download.html

2. Download the zip folder located at the intersection of the
   "HTML" row and "Packed as .zip" column.

3. Extract that Zip folder and drag it into the project's "frontend/public" folder.

4. Rename the folder to "python_docs"

You have successfully added Python Documentation for the competitors.

One last step: Run the command `mkdir -p es_files/global_docs` to avoid run-time errors due to the missing directory.

### Running the Development Server

1. `python3 -m backend.script.reset_database` to create the database and load in fake data. This can be run anytime to reset the databse.
2. Run `honcho start`
3. Open `http://localhost:4400` to view the application

## Development Concerns

### [Frontend Documentation](/docs/frontend.md)

### [Backend Documentation](/docs/backend.md)

### [Event Supervisor Documentation](/docs/event_supervisor.md)
