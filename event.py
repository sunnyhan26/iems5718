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

		event_func.addEvent(ownerid, name, my1Time, my2Time, my3Time,
			location, coordinate)
		self.response.write('Event saved successfully!')

class ViewEvent(webapp2.RequestHandler):
	def get(self):
		eventid = self.request.get('eventid')
		template_values = {
			'user': user,
		}
		template = JINJA_ENVIRONMENT.get_template('path/to/template')
		self.response.write(template.render(template_values))

class EditEvent(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'user': 'user',
		}
		template = JINJA_ENVIRONMENT.get_template('/template/Initial.html')
		self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([    
    ('/event/edit', EditEvent),  
    ('/event/view', ViewEvent),  
    ('/event/submit', SubmitEvent)
    ], debug=True)
