# "Deployment" / Exam Day Setup Instructions

Follow these instructions for exam day setup. 
Some of these only need to be completed once, but all will need to be repeated if there is an update to the software.

### Download the Repo

1. Install Docker Desktop, VSCode, and the DevContainer VSCode extension
2. Clone the repo into VSCode and open it

### Setup [Judge0](https://github.com/judge0/judge0)

*Note: This is to be completed *outside* the devcontainer

1. Download the [judge0 config file](https://github.com/judge0/judge0/blob/ffd7a48cc6da86d6ac155ef10dbd67d02736070b/judge0.conf)
2. Place the file in the `judge0` directory
3. Visit [this website](https://www.random.org/passwords/?num=1&len=32&format=plain&rnd=new) to generate a random password
4. Use this password as the `REDIS_PASSWORD` variable in the `judge0.conf` file.
5. Visit [this website again](https://www.random.org/passwords/?num=1&len=32&format=plain&rnd=new) to generate a new random password
6. Use this new password as the `POSTGRES_PASSWORD` variable in the `judge0.conf` file.

> Note: the following judge0 setup steps must be run every time you wish to run the server

7. Make sure your current working directory is set to `judge0` (`cd judge0`)
8. Run `bash start.sh` to launch the judge0 server
9. The first time you run this: put some pizza in the oven

> When you wish to exit development don't forget to stop judge0, either via `docker-compose down` inside the `judge0` directory (make sure you are outside the devcontainer!) or stopping the container in Docker Desktop.

**IMPORTANT NOTE FOR OS X USERS (And maybe others)**

Depending on your docker version, the Judge0 workers may not run properly.

To fix the issue, you need modify the Docker Group settings...

1. Locate the `settings-store.json` file (or `settings.json` for Docker Desktop versions 4.34 and earlier) at:

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

### Enter the DevContainer

For the moment, we will continue to support running the testing envrionment out of a devcontainer only.

1. Navigate back to the repo in VSCode
2. Press `Ctrl+Shift+P` on windows (`Cmd+Shift+P` on mac) to open the command pallet and run `Dev Containers: Build and Reopen in Container` (In the future to open you can just use `Dev Containers: Reopen in Container`)
3. Grab some water while the container builds

#### Download the HTML Python Documentation

1. To download the HTML Python Documentation, visit this link:
   https://docs.python.org/3/download.html

2. Download the zip folder located at the intersection of the
   "HTML" row and "Packed as .zip" column.

3. Extract that Zip folder and drag it into the project's "frontend/public" folder.

4. Rename the folder to "python_docs"

### Build the Frontend

1. `cd frontend`
2. `npm i` to install node dependencies
3. `npm run build` to build the frontend
4. `cd ..` to return to the top level directory

### Setup Environment Variables

1. `cd backend`
2. Generate a random secret key via: `openssl rand -hex 32`
3. Create a new file called `.env.development` with the following contents:

```
SECRET_KEY=<Your Generated Secret Key>
ACCESS_TOKEN_EXPIRE_MINUTES=75
```

Note that you may want to modify the `ACCESS_TOKEN_EXPIRE_MINUTES` to be longer than you test period is.
At the end of this time, the login tokens will invalidate and the user will need to log in again.

### Create Your Exam

Use the tools outlined in the [ES Documentation](event_supervisor.md) to create your exam in the `es_files` directory.

### Run the Server

Once you have finished creating your exam, you can run the server with this command, while in the home (`SOTestingEnv`) directory:

```bash
uvicorn --port=[PORT_NUMBER] --host=[HOST_NUMBER] backend.main:app 
```

Note that the port and host numbers are optional.

