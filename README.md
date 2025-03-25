# Project: Belay (a Slack clone)

A full-stack web application development using React.js, FlaskAPI, Python, PostgreSQL

<img width="1043" alt="Screenshot 2567-04-11 at 15 04 06" src="https://github.com/pannich/Belay/assets/70697272/e63812b4-6c25-438b-9e6d-ce45a6305beb">
<img width="1051" alt="Screenshot 2567-04-11 at 15 04 22" src="https://github.com/pannich/Belay/assets/70697272/1ebfa5e4-632b-4f73-9553-f09ec90cadde">


## Run Project
- cd my-react-app/backend
### `Flask run --reload --debugger`

## Directory

```
/my-react-app
    /build                # React build directory
    /static               # Flask static files (if any)
    /templates            # Flask templates (if any)
    /backend
      app.py              # Flask application here
      apply_migration.sh
    /migration
      *.sql
      belay.db
    /src                  # react components
      /Components
      ...
```

--------------------

### If need to access Dev Environment

#### React run on port 3000
```
cd my-react-app
npm install
npm start
```

#### 2. Run Backend on port 5000
```
cd my-react-app/backend
flask run --reload --debugger
```

#### 3. Database Migration
```
cd my-react-app/backend
bash apply_migrations.sh
```
#### 4. Build react
```
npm run build
```

### References

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

----------------------------------------------------------------

## Introduction

As a capstone project for Web Development, we're going to combine the various
front-end and back-end techniques we've learned over the course to produce a
modern, database-backed single-page application. Specifically, we'll be building
our own (significantly smaller in scope) version of the popular workplace
messaging app Slack. We'll call our version
[Belay](https://en.wikipedia.org/wiki/Belaying).

## Core Behavior

- Belay lets users send and read real-time chat messages that are organized into
  rooms called Channels. Users see a list of all the channels on the server and
  can click one to enter that channel. Inside, they see all the messages posted
  to that channel by any user, and can post their own messages. All messages
  belong to a channel and all channels are visible to all users; we don't need
  to implement private rooms or direct messages.
- Any user can create a new channel by supplying a display name. Channel names
  must be unique. If you wish, you may choose to limit what characters are
  allowed in channel names.
- Like Slack, messages may be threaded as Replies in response to a message in a
  channel. Messages in the channel will display how many replies they have if
  that number is greater than zero. We don't support nested threads; messages
  either belong directly to a channel or are replies in a thread to a message
  that does, but replies can't have nested replies of their own.

## Submissions and Grading

Graders will have Python 3.11+ with Flask installed, and a local install of
SQLite3 (which comes with Python). Because graders must use the same environment
to evaluate submissions from multiple students, please **do not require any
additional programs or packages to be installed**. In your submission, include a
README with instructions for how to configure and run your app:

- Graders will start your app with a `flask run` command from the command line.
  Graders will have their FLASK_APP environment variable set to "app," so name
  your Flask file `app.py`.
- Graders will have the packages in `requirements.txt` installed with
  `pip3 install -r requirements.txt`. If you feel strongly that you need a
  package not listed there, ask on the course Slack.
- Graders will try to access your app in their browser at the URL that Flask
  prints to the command line, e.g.
  `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`
- Make sure that your app starts successfully under these circumstances. We'll
  do our best to make your app run even if it doesn't, but with a points
  penalty.

You can use any techniques or tools to complete your project, whether or not we
studied them in class. In particular, note that there is no requirement that you
use React (though it may make the project easier to complete). You could do the
whole project with vanilla Javascript, you could use React, or you could use
some other framework we didn't study in class, like [Vue.js](https://vuejs.org/)
or [Svelte](https://svelte.dev/). As always, remember to include in your
submission any classmates you collaborated with and any materials you consulted.

## Requirements and Rubric (40 points total)

### Unauthenticated UI: (3 points) OK.

- OK./ Unanthenticated users can create a new account
- OK./ Unauthenticated users can sign in with their username and password
- OK./ Unauthenticed users who try to access a room cannot see any messages in that
  room, and are sent to the signup/login page instead

### Authenticated UI: (10 points) -1

- OK./ Authenticated users can log out, change their username, and change their
  password
- OK./ Authenticated users can see a list of all channels. For each channel, they
  can see how many unread messages they have in that channel
- [ ] Visiting a channel marks all messages in it as read, and all new messages
  posted to that channel while the user is in it are marked as read too
- OK./ Check for new messages in the channel at least once every 500 ms. Stop
  checking if the user leaves the channel. (Hint: use SetInterval)
- OK./ Check for new unread messages in other channels at least once every second.
  Use only one HTTP request to get counts for all channels
- OK./ For each message with replies, display the number of replies to that message
  just below the message content
- OK./ All messages in a room have a Reply button or icon that opens the replies pane
- OK./ Parse image URLs that appear in messages and display the images at the end of
  the message. (Hint: you may use the web to help you find an appropriate
  regular expression)
- OK./ Users can add an emoji reaction to any message or reply. You may choose a
  limited set of emoji reactions you support.
- OK./ Hovering over a reaction displays all the users who had that reaction

### Single-Page State (5 points) OK.

- OK./ Only serve one HTML request. Handle all other requests through the API
- OK./ Push the channel name (for messages) or parent message id (for replies) to the
  history and navigation bar when the user navigates to a channel or thread
  Users can use the Back button to navigate to a previous channel or thread
- OK./ Loading the unique URL of a channel or thread should open the app to that
  channel or thread
- OK./ If an unauthenticated user follows a link to a channel or thread, show them
  the login or signup screens, but if they log in or sign up, send them to the
  original page they requested
- OK./ Save the user's auth key in localStorage or in a cookie. Include your CNETID
  as part of your storage keys so your storage won't conflict with those of
  other students on the graders' machines. e.g.
  `window.localStorage.setItem('trevoraustin_belay_auth_key', 'abcdefg')`

### Responsive Styling: (8 points) -1

Wide Screen:

- [/] Show the list of channels down the left-hand side of the screen, and the
  channel the user is looking at (or a placeholder for no channel) on the
  right-hand side
- OK./ Clicking on the name of a channel loads that channel's messages into the
  right-hand column
- OK./ The current channel is highlighted in the channel list, and the names of other
  channels change have a subtle visual change on hover
- OK./ When viewing a reply thread, display the thread as a third column, narrowing
  the column with messages to fit it
- [/] Users can click an icon or button to dismiss the thread panel

Narrow Screens:

- OK./ On narrow screens, the page has a one-column layout with a menu bar. Users see
  the channel list, the messages in one channel, or the replies to one message
  at a time, and not the other two
- [ ] When viewing replies, users can see the parent message they are replying to.
  They can click a button or link to navigate to the channel containing the
  parent message
- OK./ When viewing messages in a channel on a narrow screen, users have a button or
  link they can click to navigate back to the channel list

### Database (8 points)

- OK./ Store channels, messages, and user account information in a SQLite3 database
- OK./ Create the database and its tables with migrations Start the name(s) of your
  migration file(s) with [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
  timestamps so that the file system will list them in the order they were
  created. Check those migrations into version control for your assignment,
  alongside the actual database file
- OK./ Create a table for channels that stores a unique id and the channel name
- OK./ Create a table for messages that stores, at a minimum, what channel the
  message is in, the id of the user that wrote the message, and its text
  contents
- OK./ Store Replies in the Messages table. Implement a way of distinguishing regular
  messages in a channel from replies to a message (e.g. with a `replies_to`
  column that is null for normal messages but contains a messsage_id for
  Replies)
- OK./ Create a table for reactions that stores, at a minimum, the emoji, the id of
  the message or comment it is a reaction to, and the id of the user who made
  the reaction
- OK./ Create a
  [join table](https://stackoverflow.com/questions/16549971/join-tables-in-sqlite-with-many-to-many)
  to capture the many-to-many relationship between Users and which Messages they
  have seen. (Hint: store the _latest_ timestamp or message id seen for each
  user in each channel—you don't have to store every user-to-message pair)
- OK./ Sanitize all database inputs by
  [passing them as arguments to a parameterized quer](https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/#:~:text=To%20pass%20variable%20parts%20to%20the%20SQL%20statement%2C%20use%20a%20question%20mark%20in%20the%20statement%20and%20pass%20in%20the%20arguments%20as%20a%20list.%20Never%20directly%20add%20them%20to%20the%20SQL%20statement%20with%20string%20formatting%20because%20this%20makes%20it%20possible%20to%20attack%20the%20application%20using%20SQL%20Injections)

### API (6 points)

- OK./ Give API endpoints a unique path namespace to distinguish them from your HTML
  path(s) e.g. `/api/endpoint1`, `/api/encpoint2` etc
- OK./ Create an authentication endpoint that accepts a username and password, and
  returns a session token
- [/] Authenticate to other endpoints via session token in the request header (not
  as a URL param or in a request body)
- OK./ Use GET requests for API calls that don't change data on the server, and POST
  requests for API calls that **do** change data on the server
- OK./ Create endpoints to create and get channels and messages, and to update a user's last
  read message in a channel
- OK./ Create an endpoint to return unread message counts for the user for each channel in a
  single request with a single database query

----------------------
