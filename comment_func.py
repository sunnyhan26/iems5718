from google.appengine.ext import ndb    

class Comment(ndb.Model):
	user = ndb.UserProperty(auto_current_user=True)
	content = ndb.TextProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)

def addComment(user, content, time):
	comment = Comment(user=user, content, time)
	comment.put()

def getCommentList():
