import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users

class User(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	lastLoginDate = ndb.DateTimeProperty(auto_now_add=True)

def getCurrentUser(requestHandler):
	user = users.get_current_user()
	if user:
		addUser(user.user_id(), user.email(), user.nickname())
	else:
		requestHandler.redirect(users.create_login_url(requestHandler.request.uri))
	return user
	

def addUser(user_id, email, name):
	user = User(key=ndb.Key('User', user_id), email=email, name=name)	
	user.put()

def getUserInfo(user_id):
	userkey = ndb.Key('User', user_id)
	user = userkey.get()
	return user
	
def getUserList():
	query = User.query()
	userlist = [] 
	for result in query.iter():
		userlist.append(result.name)
	return userlist

