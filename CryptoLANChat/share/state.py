# share/state.py

# online kullanıcılar (id -> username)
online_users = {}

def user_online(user_id, username):
    online_users[user_id] = username

def user_offline(user_id):
    online_users.pop(user_id, None)
