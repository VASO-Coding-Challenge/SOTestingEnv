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