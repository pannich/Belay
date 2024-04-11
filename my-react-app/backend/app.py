import string, random, os
from flask import *
import sqlite3
from flask_cors import CORS


app = Flask(__name__, static_folder='../build', static_url_path='')
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('../migration/belay.db' , timeout=30)
        db.row_factory = sqlite3.Row
        setattr(g, '_database', db)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cursor = db.execute(query, args)
    rows = cursor.fetchall()
    db.commit()
    cursor.close()
    if rows:
        if one:
            return rows[0]
        return rows
    return None

def get_user_from_token(request):
    token = request.headers.get('Authorization')
    return query_db('select * from users where session_token = ?', [token], one=True)

def update_token(user_id, newtoken):
    user = query_db('UPDATE Users SET session_token = ? WHERE id = ? RETURNING *', (newtoken, user_id), one=True)
    return user

# Authenticate USER API
def require_api_key(f):
    """a decorator function to check user api key
    Check if the requested API header 'X-API-Key' matches with current user html cookie.
    """
    def decorated_function(*args, **kwargs):
        user = get_user_from_token(request)
        if user: # There's X-API-KEY in header and user matches this key exists
            print("API check: ", user, user['session_token'])
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid or missing API key."}), 400
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_user_from_id(user_id):
    return query_db('select * from Users where id = ?', [user_id], one=True)

# ------------------- FROM REACT FRONTEND -------------------------

# @app.route('/')
# def index():
#     return "Messaging App API. Go to port 3000 for FrontEnd."

# from React
@app.route('/')
@app.route('/profile')
@app.route('/login')
@app.route('/channel')
@app.route('/channel/<ch_id>')
def serve(ch_id=None):
    print("get here")
    return app.send_static_file('index.html')

# ------------------- API -------------------------

@app.route('/api/auth', methods=['POST'])
def authenticate():
    """
    Path: /api/auth
    Method: POST
    Description: Accepts a username and password, authenticates the user, and returns a session token.
    Request Body: { "username": "user", "password": "pass" }
    Response: { "token": "session_token" }

    """
    session_token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        try:
            user = query_db('''
        SELECT *
        FROM Users
        WHERE username = ? and password = ?
        ''', [username, password], one=True)
            if user:
                # user exists, user can login
                # update sessionn token in user database
                user = update_token(user['id'], session_token)
                return jsonify({
                    'message': "User login",
                    'username': user['username'],
                    'password': user['password'],
                    'id': user['id'],
                    'token': user['session_token']}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# ------------------- PROFILE -------------------------

# api for signing up -> return API-KEY
@app.route('/api/signup', methods=['POST']) #TODO ? create GET for when existing user /signup
def signup():
    """User coming in without Authentication. Sign up with username, password.
    """
    print("signup")

    session_token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        try:
            user = query_db('''
        INSERT INTO Users (username, password, session_token)
        VALUES (?, ?, ?) returning *
        ''', [username, password, session_token], one=True)
            return jsonify({"message": "Signed up successfully", "username": user['username'], "password": user['password'], "session_token": user['session_token']}), 200
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Username already taken. For existing user, go to Login.'}), 400
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Browswer coming in without API-KEY. Log in finds API-KEY that matches input username, password
"""
    # go to authenticate and return session token
    return authenticate()

@app.route('/api/logout', methods=['POST'])
def logout():
    """remove session token"""
    print("gethereeeee")
    user = get_user_from_token(request)
    print(user)

    try :
        update_token(user['id'], '')
        return jsonify({'message': 'User logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# POST to change the user's name
@app.route('/api/user/change-username', methods=['POST'])
@require_api_key
def update_username():
    user = get_user_from_token(request)
    if not user: return jsonify({'error': 'User not found'}), 403

    # get new name
    if request.method == 'POST':
        data = request.get_json()
        new_username = data.get('newUsername')

        try:
            new_user = query_db('''
        UPDATE Users
        SET username = ?
        WHERE id = ? RETURNING *
        ''', (new_username, user['id']), one=True)
            return jsonify({'message': f"Username: {new_user['username']} updated successfully",
                            "username": new_user["username"]}), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# POST to change the user's password
@app.route('/api/user/change-password', methods=['POST'])
@require_api_key
def update_password():
    user = get_user_from_token(request)
    if not user: return jsonify({'error': 'User not found'}), 403

    # get new password
    if request.method == 'POST':
        data = request.get_json()
        new_password = data.get('newPassword')

        try:
            new_user = query_db('''
        UPDATE Users
        SET password = ?
        WHERE id = ? RETURNING *
        ''', (new_password, user['id']), one=True)
            return jsonify({'message': f"Username: {new_user['password']} updated successfully",
                            "username": new_user["username"],
                            "password": new_user["password"]}), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# ------------------- CHANNELS -------------------------

@app.route('/api/channels', methods=['POST'])
@require_api_key
def create_channel():
    """_summary_
    Description: Creates a new channel.
    Request Header: `Authorization: Bearer session_token` ## ASK?
    Request Body: { "name": "channel_name" }
    Response: { "id": channel_id, "name": "channel_name" }
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
        try:
            new_channel = query_db('''
        INSERT INTO Channels (name)
        VALUES (?) returning *
        ''', [name], one=True)
            return jsonify({"message": "Channel created successfully", "id": new_channel['id'], "name": new_channel['name']}), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# not used use unread_count api
# @app.route('/api/channels', methods=['GET'])
# # @require_api_key
# def get_channels():
#     channels = query_db('SELECT * FROM Channels', one=False)
#     return jsonify([{'id': channel['id'], 'name': channel['name']} for channel in channels]), 200

# updating last read
@app.route('/api/channels/<int:channelId>/updateLastSeen', methods=['POST'])
@require_api_key
def update_last_message_seen(channelId):
    """
    Description: update last message id seen
    Request Header: `Authorization: Bearer session_token`
    Request Body: { "channel_id": channel_id, "user_id": user_id, "last_message_id_seen": "last_message_id_seen"}
    Response: # TODO RESPONSE
    """
    if request.is_json:
        data = request.get_json()
        channel_id = data.get('channel_id')
        user_id = data.get('user_id')
        last_message_id_seen = data.get('last_message_id_seen')

    try:
        # query channel_id , and timestamp to find message_id
        message = query_db('''
        SELECT 1 FROM Users_Messages_Seen WHERE user_id = ? AND channel_id = ?
        '''
        , [user_id, channel_id], one=True)

        if message:
            # If a record exists, update it with the new last_message_id_seen
            query_db('UPDATE Users_Messages_Seen SET last_message_id_seen = ? WHERE user_id = ? AND channel_id = ?', (last_message_id_seen, user_id, channel_id), one=True)
        else:
            # If no record exists, insert a new one
            query_db('INSERT INTO Users_Messages_Seen (user_id, channel_id, last_message_id_seen) VALUES (?, ?, ?)', (user_id, channel_id, last_message_id_seen))
        return jsonify({'message':'updated latest message seen'})

    except Exception as e:
        return jsonify({'error': f'An error occurred while updating last message seen: {e}'}), 500
    return

# ------------------- messages -------------------------

@app.route('/api/messages', methods=['POST'])
@require_api_key
def post_message():
    """
    Request Header: `Authorization: Bearer session_token`
    Request Body: { "channel_id": channel_id, "content": "message_content", "replies_to": null or message_id }
    Response: { "id": message_id, "content": "message_content", "channel_id": channel_id, "user_id": user_id, "timestamp": "datetime", "replies_to": null or message_id }

    """

    if request.is_json:
        data = request.get_json()
        user_id = data.get('user_id')
        channel_id = data.get('channel_id')
        content = data.get('content')
        replies_to = data.get('replies_to', None)
    try:
        message = query_db('''
        INSERT INTO Messages (channel_id, user_id, content, replies_to)
        VALUES (?, ?, ?, ?) RETURNING *
        ''', (channel_id, user_id, content, replies_to), one=True)
        print(message)

        return jsonify({"message": "Message posted successfully", "id": message['id'], "content": message['content'], "channel_id": message['channel_id'], "user_id": message['user_id'], "timestamp": message['timestamp'], "replies_to": message['replies_to']}), 201
    except Exception as e:
        return jsonify({'error': 'An error occurred while posting messages'}), 500


##### CAN ADD replies FIELD TO GET MESSAGE ?
@app.route('/api/messages', methods=['GET'])
@require_api_key
def get_messages():
    """
    Description: Get all the messages in a room
    Request Header: `Authorization: Bearer session_token`
    Request Body: { "channel_id": channel_id }
    Response: # TODO CHECK
    [{ "id": message_id, "username": "username", "content": content, "user_id": user_id, "timestamp": "datetime", "replies_to": null or message_id },
    ...]

    """
    print("get message ")

    channel_id = request.args.get('channel_id')  # Assuming you pass room_id as a query parameter

    if not channel_id:
        return jsonify({'error': 'Channel ID not found'}), 400

    try:
        messages = query_db('select * from Messages where channel_id = ? AND replies_to IS NULL', [channel_id], one=False)
        # print(channel_id, messages)
        if not messages:
            return jsonify({'message': 'no message found'}), 200
        ls_messages = []
        for message in messages:
            user = get_user_from_id(message['user_id'])
            if not user:
                print("user id not found")
                continue
            # TODO check what to return
            ls_messages.append({'id': message['id'], 'username': user['username'], "timestamp": message['timestamp'], 'content': message['content']})
        # print(ls_messages)
        return jsonify(ls_messages), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred while fetching messages: {e}'}), 500

# TODO testing
@app.route('/api/messages/unread_counts', methods=['GET'])
def unread_counts():
    """fetch all channels and unread counts"""
    user_id = 1

    unread_by_channel = query_db("""
SELECT
    Channels.id AS channel_id,
    Channels.name,
    IFNULL(UnreadMessages.unread_count, 0) AS unread_count
FROM
    Channels
LEFT JOIN (
    SELECT
        Messages.channel_id,
        COUNT(Messages.id) AS unread_count
    FROM
        Messages
    LEFT JOIN Users_Messages_Seen
        ON Messages.channel_id = Users_Messages_Seen.channel_id
        AND Users_Messages_Seen.user_id = ?  -- Named placeholder
    WHERE
        Messages.id > Users_Messages_Seen.last_message_id_seen
        OR Users_Messages_Seen.last_message_id_seen IS NULL
    GROUP BY
        Messages.channel_id
) AS UnreadMessages ON Channels.id = UnreadMessages.channel_id
""", [user_id], one=False)
    channels_list = []
    if not unread_by_channel:
        return jsonify(channels_list), 200
    for channel in unread_by_channel:
        channel_dict = {
            'id': channel["channel_id"],
            'name': channel["name"],
            'unread_count': channel["unread_count"]
        }
        channels_list.append(channel_dict)
    return jsonify(channels_list), 200


@app.route('/api/messages/replies_to', methods=['GET'])
@require_api_key
def replies_to_messages():
    """
    Description: Get replied messages for a particular message_id
    Request Header: `Authorization: Bearer session_token`
    Request Body: { "channel_id": channel_id, 'author': user['username'], "message_id": "message_id"}
    Response: # TODO CHECK
    { "id": message_id, "replies": [array of replies to this messages_id] }

    """
    # do querying
    ##### CAN ADD replies FIELD TO GET MESSAGE ?
    channel_id = request.args.get('channel_id')  # Assuming you pass room_id as a query parameter
    message_id = request.args.get('message_id')

    try:
        replies = query_db('select * from Messages where channel_id = ? AND replies_to = ?', [channel_id, message_id], one=False)
        # print(channel_id, messages)
        if not replies:
            return jsonify({'message': 'no message found'}), 200
        ls_replies = []
        for message in replies:
            user = get_user_from_id(message['user_id']) # get author
            if not user:
                print("user id not found")
                continue
            # TODO check what to return
            ls_replies.append({'id': message['id'], 'username': user['username'], 'content': message['content'], 'timestamp': message['timestamp'], })
        # print(ls_messages)
        return jsonify(ls_replies), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred while fetching messages: {e}'}), 500

# ------------------- emoji -------------------------

@app.route('/api/messages/emoji', methods=['POST'])
@require_api_key
def create_reaction():
    """
    Description: insert new emoji added by userX
    Request Header: `Authorization: Bearer session_token` ## ASK?
    Request Body: { "emoji": "emoji" , "message_id" : "message_id", "user_id": "user_id"}
    Response: { "message" : f"emoji {emoji} add to {message_id} successfully" }, 200

    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            emoji = data.get('emoji')
            message_id = data.get('message_id')
            user_id = data.get('user_id')
        try:
            new_reaction = query_db('''
        INSERT INTO Reactions (emoji, message_id, user_id)
        VALUES (?, ?, ?) returning *
        ''', [emoji, message_id, user_id], one=True)
            return jsonify({"message": f"Emoji {emoji} add to {message_id} successfully"}), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/api/reactions/users', methods=['GET'])
@require_api_key
def get_reaction():
    """
    Description: get user names from message_id and emoji
    Request Header: `Authorization: Bearer session_token` ## ASK?
    Request Body: { "emoji": "emoji" , "message_id" : "message_id"}
    Response: [user1, user2, user3, ... ], 200

    """
    emoji = request.args.get('emoji')
    message_id = request.args.get('message_id')

    try:
        users_reaction = query_db('''
    SELECT * FROM Reactions
    WHERE emoji=? AND message_id=?
    ''', [emoji, message_id], one=False)
        if users_reaction:
            users = []
            for row in users_reaction:
                user = get_user_from_id(row['user_id'])
                users.append(user['username'])
            print(users)
            return jsonify(users), 200
        else:
            return jsonify([]), 200

    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
