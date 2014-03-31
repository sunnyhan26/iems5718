import webapp2
from google.appengine.ext import ndb    

class User(ndb.Model):
	email = ndb.StringProperty()
	name = ndb.StringProperty()
	lastLoginDate = ndb.DateTimeProperty(auto_now_add=True)

def addUser(user_id, email, name):
	user = User(key=ndb.Key('User', user_id), email=email, name=name)	
	user.put()

def getUserInfo(user_id)
	userkey = ndb.Key('User', user_id)
	user = userkey.get()
	return user
	
def getUserList()
	query = User.all()
	userlist = query.fetch()
	return userlist

