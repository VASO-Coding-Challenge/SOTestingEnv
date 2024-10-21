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


#### Authentication - JWT

Ensure that you have these packages installed: `pip3 install pyjwt` to ensure your project works well with the authorization system. Navigate to your `backend` folder and create yourself a `.env.development`. You will need to run the following command to generate yourself a secret key: `openssl rand -hex 32`. To confirm that the route works as expected, clear your database and run the test data generated for the `teams.py` test data.

The format for the `.env.development` file is:

SECRET_KEY=[Your Generated Secret Key]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


#### FastAPI

When creating FastAPI routes, make sure to define the routes in a feature file named corresponding to the feature inside of the `api` directory.
This file should look similar to the example one in `api/count.py`. You will need to import the file in `main.py` and
add it to the `feature_apis` list as well as the tags in the `openapi_tags` list in the `FastAPI()` constructor.

#### SQLModel

Define all SQLModels in the `models` folder in a file named according to the feature. Make sure to add this file to the `__all__` list inside
of the `__init__.py` file in the `models` folder. This will allow it to be imported by default inside of the `create_database` script.

In the future we will support adding fake data inside of the `create_database` script.
