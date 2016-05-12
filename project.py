#importing from foreign libraries
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#importing from my own files
from database_setup import Base, Institution, User, OrganicUser
from hostdetails import host, path_to_repo

app = Flask(__name__)
app.secret_key = 'super_secret_key'

#attaching to DB
DB= 'sqlite:///'+path_to_repo+'users.db'
engine = create_engine(DB)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

company_name = "EmpowerK12"

CLIENT_ID = json.loads(
    open(path_to_repo+'client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = company_name

#Login Page
@app.route('/')
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    #This is to make sure no scripts are being run which can replace clicking of the google sign button
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        #oauth_flow = flow_from_clientsecrets('/home/vgoel38/EmpowerK-12/client_secrets.json', scope='')
        oauth_flow = flow_from_clientsecrets(path_to_repo+'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 201)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['access_token'] = access_token

    #see if user already exists, if not make a new one
    user_id = getUserID(login_session['email'])
    print login_session['email']
    if not user_id:
        print "accessing/making organic id"
        organic_user_id = getOrganicUserID(login_session['email'])
        if not organic_user_id:
            createOrganicUser(login_session)
        login_session['user_id'] = organic_user_id
        return userUnautorizedAccess()
    else :
        login_session['user_id'] = user_id

    response = make_response(json.dumps({'username': login_session['username'],'image_source': login_session['picture']}, sort_keys=True, indent=4, separators=(',', ': ')), 200)
    response.headers['Content-Type'] = 'application/json'

    # output = ''
    # output += '<h1>Welcome, '
    # output += login_session['username']
    # output += '!</h1>'
    # output += '<img src="'
    # output += login_session['picture']
    # output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    print response
    return response

# User Helper Functions
def createOrganicUser(login_session):
    newUser = OrganicUser(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(OrganicUser).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def getOrganicUserID(email):
    try:
        user = session.query(OrganicUser).filter_by(email=email).one()
        return user.id
    except:
        return None

def deleteSessionDetails():
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: '
    print login_session.get('username')
    if access_token is None:
        print 'Access Token is None'
        return '401'
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

    print "result status is" + result['status']

    return result['status']


@app.route('/gdisconnect')
def gdisconnect():

    statusCode = deleteSessionDetails()
    print statusCode

    if statusCode == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    elif statusCode == '401':
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'

    return response

    #return render_template('goodbye.html', response = response)


def userUnautorizedAccess():

    statusCode = deleteSessionDetails()
    print statusCode

    if statusCode == '200':
        print "blah"
        response = make_response(json.dumps('User Unauthorized to login.'), 401)
        response.headers['Content-Type'] = 'application/json'
    # elif statusCode == '401':
    #     response = make_response(json.dumps('Current user not connected.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'

    return response


#User Account Details
@app.route('/myaccount')
def showAccountDetails():
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('myaccount.html', name=login_session['username'], picture=login_session['picture'], email=login_session['email'])


#Memory Videos
@app.route('/memory')
def showMemoryVideos():
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('memory.html')


#All courses
@app.route('/courses')
def showCourses():
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('courses.html')

#Memory Workshop
@app.route('/memoryworkshop')
def showMemoryWorkshop():
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('memoryworkshop.html')

#webinars
@app.route('/webinars')
def showWebinars():
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('webinars.html')

#android
@app.route('/android')
def showAndroid():
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('android.html')


if __name__ == '__main__':
    app.debug = True
    if host == 'localhost':
        app.run(host='0.0.0.0', port=5000)