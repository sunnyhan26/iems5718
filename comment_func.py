from google.appengine.ext import ndb    

class Comment(ndb.Model):
	user = ndb.UserProperty(auto_current_user=True)
	content = ndb.TextProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)

def addComment(eventid, content):
	comment = Comment(parent=ndb.Key('Event', int(eventid)), content=content)
	comment.put()

def getCommentList(eventid, startcid, commentno):
	pass
