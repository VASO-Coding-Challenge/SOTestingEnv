# Testing Guide

It's very important for us to ensure our functionality is correct and in working order.
Please follow this guide when creating new features to ensure that the feature works as intended.

## What to test?

Since time is limited, we want to prioritize testing only the core functionality of our project, so we intend on only testing the code found in the `backend/services` folder. If time permits, we would also like to test code in the `backend/script` folder.
Please note that we do not have any current plans to write tests for the frontend.

Our goal is to reach 100% code coverage on the `backend/services` folder which we can check (and see which lines we are missing) via the following command:

```zsh
coverage run --source=backend.services -m pytest -v backend/test && coverage report -m
```

## How to Test?

### Step 1: Create Service Fixture

Select a service class in the `backend/services` directory to test. Ensure that there is a fixture defined for that class in `test/fixtures.py`.
A fixture is pytest functionality that is managed to ensure each test is run in its own individual context.
If your service needs access to the database, you can request the `session` via the `session` fixture defined in `conftest.py` like so:

```python
@pytest.fixture()
def my_svc(session: Session):
    # Any additional code you need here
    return MyService(session)
```

> Click [here](https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are) if you would like to learn more about fixtures. Suggested reading is through the section on scope.

### Step 2: Set Up Test Data

Tests aren't complete without test data! Let's define some for our new service (assuming we need data for this service) in the `backend/test/fake_data` directory.
Use the model you intend on inserting into the database to create some top-level instances such as:

```python
person1 = Person(firstname="Cindy", lastname="Loohoo")
```

Next, after you have defined your data, write a function that takes in a session and adds all of the test data to that session. There is no need to commit in this function.
Finally, write a new fixture that requests the `session` fixture, runs the function we just created, and finally commits the data to the database.
In this fixture, make sure to request any other data fixtures that this one will depend on so they can be inserted first.
This would look something like:

```python
def add_data(session: Session):
    for data in datas:
        session.add(data)

@pytest.fixture()
def add_data_fixture(data_i_need_fixture, session: Session):
    add_data(session)
    session.commit()
```

While you're at it, it might be helpful if you also add this data to the `reset_database` script!

### Step 3: Write some tests!

Now that we have our fixtures defined and our test data set up, we can start writing some tests!
First, create a new file corresponding to the service you'd like to test, with the suffix `_test.py`. (Ex: `my_svc_test.py`)
This suffix is needed so pytest knows you are using this as a test function!

In that file, go ahead and import the following:

- Any test data fixtures you will want to use in your tests
- The pytest module
- Any exceptions that your service raises
- Anything else you need to run your tests

Next, its time to actually write the tests!
Start by writing a function with the prefix `test_` (again so pytest knows this is a test function).
Make sure to name it something relevant and include a docstring indicating exactly what you are trying to test.
In the signature, call any fixtures you would like to use including the service fixture and the data fixtures.

To write the tests, make sure to analyze the input and outputs of the method you're testing as well as the code branching structure.
Perform your method on some sample test data, then use `assert` statments ensure the output is what we expect.
If you're testing for a raised exception use `while pytest.raises(<ExceptionName>)`.
A finished test should look something like this:

```python
def test_method_working(my_svc, add_data_fixture):
    did = my_svc.do_something(1,2)
    assert did = 12

def test_method_throws(my_svc, add_data_fixture):
    with pytest.raises(ValueException): # this will fail the test if the exception is not thrown
        my_svc.do_something("foo", "bar")
```

## Further Testing Concerns

These concerns may need to be utilized and elaborated further in this section:

- Spying
- Mocking
