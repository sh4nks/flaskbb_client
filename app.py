import os
from flask import Flask, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from flask_script import Manager, Shell, Server

CLIENT_ID = 'u06X2qzc5KW5vgKwGP29avEH5OtpJynLOGqxuIaU'
CLIENT_SECRET = 'zBArOaBonKuHZt6aCycsjFmSX7RAlq79VYYwZiO0eSg7eRN6ht'

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret'
oauth = OAuth(app)

remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'user'},
    base_url='http://localhost:8080/api/v1/',
    request_token_url=None,
    access_token_url='http://localhost:8080/oauth/token',
    authorize_url='http://localhost:8080/oauth/authorize'
)


@app.route('/')
def index():
    if 'remote_oauth' in session:
        resp = remote.get('users')
        return jsonify(resp.data)
    next_url = request.args.get('next') or request.referrer or None
    return remote.authorize(
        callback=url_for('authorized', next=next_url, _external=True)
    )


@app.route('/authorized', methods=["GET", "POST"])
def authorized():
    resp = remote.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['remote_oauth'] = (resp['access_token'], '')
    return jsonify(oauth_token=resp['access_token'])


@remote.tokengetter
def get_oauth_token():
    return session.get('remote_oauth')


# Debug settings
os.environ['DEBUG'] = 'true'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

manager = Manager(app)
# Run local server
manager.add_command("runserver", Server("localhost", port=8000))


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
