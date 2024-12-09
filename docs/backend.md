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