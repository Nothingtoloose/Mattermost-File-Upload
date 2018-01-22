SERVER_URL = "http://localhost:80/"
CHANNEL_ID = "dzs4hiqeghgfh"
USER_EMAIL = "test"
USER_PASS = "test"
FILE_PATH = '/home/localadmin/Schreibtisch/Test.md'

import requests, json, os

# Login
s = requests.Session() # So that the auth cookie gets saved.
s.headers.update({"X-Requested-With": "XMLHttpRequest"}) # To stop Mattermost rejecting our requests as CSRF.

l = s.post(SERVER_URL + 'api/v4/users/login', data = json.dumps({'login_id': USER_EMAIL, 'password': USER_PASS}))

USER_ID = l.json()["id"]

# Upload the File.
form_data = {
        "channel_id": ('', CHANNEL_ID),
        "files": (os.path.basename(FILE_PATH), open(FILE_PATH, 'rb')),
}
r = s.post(SERVER_URL + 'api/v4' + '/files', files=form_data)

FILE_ID = r.json()["file_infos"][0]["id"]

# Create a post and attach the uploaded file to it.
p = s.post(SERVER_URL + 'api/v4' + '/posts', data = json.dumps({
    'user_id': USER_ID,
    'channel_id': CHANNEL_ID,
    'message': 'Post message goes here',
    'file_ids': [FILE_ID,],
}))
