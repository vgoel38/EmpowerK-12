from flask import Flask, render_template
from flask import session as login_session
import random, string

application = Flask(__name__)
@application.route('/')
@application.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.secret_key = 'super_secret_key'
    application.debug = True
    application.run('0.0.0.0')