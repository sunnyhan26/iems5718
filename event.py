import webapp2
import event_func
import user_func
from google.appengine.api import users

import os
# import module for templates
import jinja2
# for logging message to server log
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SubmitEvent(webapp2.RequestHandler):
	def post(self):
		ownerid = users.get_current_user().user_id()
		name = self.request.get('name')
		summary = self.request.get('introduction')
		my1Time = self.request.get('my1Time')
		my2Time = self.request.get('my2Time')
		my3Time = self.request.get('my3Time')
		location = self.request.get('location')
		coordinate = self.request.get('coordinate')
		eventid = self.request.get('eventid')

		logging.info('Received event submit rquest: ' +
			ownerid + ', ' + name + ', ' + summary + ',' + my1Time + ', ' +
			my2Time + ', ' + my3Time + ', ' + location + ', ' + coordinate +
			', ' + eventid)


		splitted = coordinate.split(',')
		lagitude = float(splitted[0])
		longitude = float(splitted[1])

		event_func.addEvent(ownerid, name, summary, my1Time,
			my2Time, my3Time,
			location, lagitude, longitude, eventid)
		self.response.write('Event saved successfully!')

class SubmitVote(webapp2.RequestHandler):
	def post(self):
		userid = users.get_current_user().user_id()
		eventid = self.request.get('eventid')
		voteList = self.request.get('voteList')
		voteEvent(eventid, userid, voteList)
		self.response.write('Vote saved successfully!')

def getCommentList():
	commentlist=[]
	commentlist.append(["1","2","3"])
	commentlist.append(["1","2","3"])
	return commentlist

def listCountNonNone(list):
	count = 0
	for i in list:
		if i is not None:
			count += 1
	return count

class ViewEvent(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		eventid = self.request.get('eventid')
		logging.info('Received view event request with eventid ' + eventid)
		try:
			event = event_func.getEvent(int(eventid))
		except ValueError:
			event = event_func.getEvent(5066549580791808)
		datelist = [event.my1Time, event.my2Time, event.my3Time]
		length = listCountNonNone(datelist)
		votelist = event_func.getVoteList(int(eventid), None)
		chosenlist = event_func.getVoteList(int(eventid), user.user_id()) 
		commentlist = getCommentList()
		template_values = {
			'eventname': event.name,
			'location': event.location,
			'introduction' : event.summary,
			'datelist': datelist,
			'length' : length,
			'votelist': votelist,
			'chosenlist': chosenlist,
			'commentlist': commentlist,
			'lat':event.lagitude,
			'long':event.longitude
		}
		if event.ownerid == user.user_id():
			template = JINJA_ENVIRONMENT.get_template('/template/initial.html')
		else:
			template = JINJA_ENVIRONMENT.get_template('/template/view.html')
		self.response.write(template.render(template_values))

class EditEvent(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)

		template_values = {
			'user': user,
		}
		template = JINJA_ENVIRONMENT.get_template('/template/initial.html')
		self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([    
    ('/event/edit', EditEvent),  
    ('/event/view', ViewEvent),  
    ('/event/submit', SubmitEvent),
    ('/event/submitvote', SubmitVote),
    ], debug=True)
