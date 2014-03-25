import webapp2
from google.appengine.ext import ndb    

class Comment(ndb.Model):
	user = ndb.UserProperty(auto_current_user=True)
	comment = ndb.TextProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)

