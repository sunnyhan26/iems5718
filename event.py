import webapp2
import event_func
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
		my1Time = self.request.get('my1Time')
		my2Time = self.request.get('my2Time')
		my3Time = self.request.get('my3Time')
		location = self.request.get('location')
		coordinate = self.request.get('coordinate')
		eventid = self.request.get('eventid')

		logging.info('Received event submit rquest: ' +
			ownerid + ', ' + name + ', ' + my1Time + ', ' + my2Time +
			', ' + my3Time + ', ' + location + ', ' + coordinate +
			', ' + eventid)

		event_func.addEvent(ownerid, name, my1Time, my2Time, my3Time,
			location, coordinate, eventid)
		self.response.write('Event saved successfully!')

def getdatelist():
	datelist = [
		'2014-04-08',
		'2014-04-09',
		'2014-04-26'
		]
	return datelist

def getvotelist():
	votelist = [ 12, 24, 36 ]
	return votelist


class ViewEvent(webapp2.RequestHandler):
	def get(self):
		eventid = self.request.get('eventid')
		logging.info('Received view event request with eventid' + eventid)
		datelist = getdatelist()
		votelist = getvotelist()
		chosenlist = [True, False, True]
		template_values = {
			'datelist': datelist,
			'votelist': votelist,
			'chosenlist': chosenlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/view.html')
		self.response.write(template.render(template_values))

class EditEvent(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
				# redirect "/" after user has logged out
				logout_url = users.create_logout_url('/')
		else:
				# direct to login and redirect back to this page after login
				self.redirect(users.create_login_url(self.request.uri))
				# return will stop loading code below
				return

		template_values = {
			'user': user,
		}
		template = JINJA_ENVIRONMENT.get_template('/template/initial.html')
		self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([    
    ('/event/edit', EditEvent),  
    ('/event/view', ViewEvent),  
    ('/event/submit', SubmitEvent)
    ], debug=True)
