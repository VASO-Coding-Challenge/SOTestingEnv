# Using the Semester 1 Version of SOTestingEnv

## Finding the Version in git

The correct version is the tag "v0.2.0". To get that version of the code, first create a separate clone of the repository, and in that working copy run the command "git checkout v0.2.0". That will set the working copy to look at the files as they were at the end of the first semester, plus a few changes I made before the second semester crew started working. However, it puts the working copy in a strange state called a "detached HEAD," meaning you effectively can't make any changes. That's why creating a separate working copy is useful.

## Fixing Things Up to Run in a Tournament

### Linux Networking Fix

Based on this answer:

> https://stackoverflow.com/questions/48546124/what-is-the-linux-equivalent-of-host-docker-internal

change `backend/services/submissions.py` by replacing `host.docker.internal` with `172.1X.0.1` where X is the first of 7, 8, or 9 that works. (8 worked for Saba.)

### Accessing the Server from Another Machine

By default, the web app is accessible only from localhost. To fix this, first edit `Caddyfile` by changing this line:

```http://localhost:4400 {```

to this:

```http://127.0.0.1:4400, http://localhost:4400, :4400 {```

Then in `.devcontainer/devcontainer.json` add this line after the forwardPorts line:

```"appPort": ["4400:4400"],```

### Loading the Monaco Editor from Local Storage

The code editor component (called Monaco) used for displaying and editing Python code has an external dependency that by default requires an internet connection. To instead load the dependency from local files, make the following changes:

```pushd frontend ; cp -R node_modules/monaco-editor public/ ; popd```

(Ideally, that should happen whenever we do the `npm install`, so we need to modify the readme.md file accordingly at some point.)

Then edit the file `frontend/src/components/SubmissionWidget.tsx`. First, change this line:

```import { Editor } from "@monaco-editor/react";```

to

```import { Editor, loader } from "@monaco-editor/react";```

and then add the following line just before line 34 (the line starting with `const [activeTab, setActiveTab]`):

```loader.config({ paths: { vs: '/monaco-editor/min/vs' } });```

(Again, this should eventually be made permanent in the code base.)

These instructions are based on this answer:

> https://github.com/suren-atoyan/monaco-react/issues/168

### Write-Only Submission Files Bug

Unfortunately, the relationship between the app and submission files is write-only. It seems to keep existing submissions cached in the browser, but never reads from the files in the submissions folder, only writes to them. Logging in again after clearing cookies/cache/etc results in a blank test on the front end, even though the old submissions are stored in the files. This would cause issues if two different computers log in as the same team.

The work-around is to tell teams to either use only one computer (e.g., one student does all the coding problems), or to do all work on a problem from the same computer (e.g., one student does all the odd problems and the other does all the evens).

### Initial Display Bug

On some browsers, the display of the test always starts with the left panel showing problem 1 selected, but the main panels are on problem 2. (This happens for Saba, but not for Ian.) This is easily corrected by simply clicking on another question in the left panel.

### Linux cgroups Fix

Edit the file `/etc/default/grub`:

Change this line:

```GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"```

to say this instead:

```GRUB_CMDLINE_LINUX_DEFAULT="systemd.unified_cgroup_hierarchy=0 quiet splash"```

Save the changes and exit your editor. Then, run the following command to update grub:

```sudo update-grub```

These instructions are based on this answer:

> https://askubuntu.com/questions/1399741/trying-to-fix-docker-cgroup-doesnt-match-target-mode-with-adding-kernel-boot.



## Setting up the teams

Run these two commands to create a brand new database with no teams:

```
python3 -m backend.script.reset_database
python3 -m backend.script.reset_teams
```

Now run through the procedure in one of the following sub-sections.

### Setting up the teams for testing

For testing, run this to make a few sample teams that run all day.
(Change the date to today.)

```python3 -m backend.script.add_teams C 5 03/08/2025 00:01 23:59```

Your team settings are now ready for testing.

### Setting up the teams for the state tournament

For the real thing, you will run these three commands, but first adjust the times in the second and the third to account for a little time at the beginning and end of the testing period. The times given allow 5 minutes at each end, but adjust as you like. Now run the adjusted commands:

```
python3 -m backend.script.add_teams C 29 03/29/2025 00:01 23:59
python3 -m backend.script.add_teams C 10 03/29/2025 11:55 12:40
python3 -m backend.script.add_teams C 10 03/29/2025 13:05 13:50
```

Open this web page to see who is signed up in each session:

> https://virginiaso.knack.com/vaso-division-bc-portal#tournaments/tournament-details/64da834d6be5ac0026224bf8/trial2-c/64da834d6be5ac0026224bf8/

The sign-up is open until just before the tournament. Sign-ups close (I think) on the day before, so you'll have to do this setup at that time to get them all.

Now edit `es_files/teams/teams.csv` as follows:

- Delete the C29 row. (There are only 28 teams.)
- Now search-and-replace to replace "00:01 23:59" with "11:55 12:40" for the teams in session 3, and then "00:01 23:59" with "13:05 13:50" for the teams in session 4. (If you changed the times above, change them here too.)
- If any of the C1-C28 teams remain with the "00:01 23:59" times, delete them.

Now, at the tournament, use the C30-C39 teams for anyone who shows up in session 3 that either didn't sign up or signed up in session 4. (And use teams C40-C49 similarly in session 4.)

Finally, run this command to reflect your edits into the database:

```python3 -m backend.script.teams_to_db```

Your team settings are now ready for the competition, and you can use `es_files/teams/teams.csv` to do a mail merge to create login hand-outs for the students.

### Updating the Testing Times

Edit the teams.csv file to change the test times as you wish, then run this command:

```python3 -m backend.script.teams_to_db```



## Creating questions

This command adds one blank question, ready for editing:

```python3 -m backend.script.generate_blank_questions 1```
