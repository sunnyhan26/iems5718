import webapp2
from google.appengine.api import users

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
		date = self.request.get('date')
		location = self.request.get('location')
		time = self.request.get('time')

	addEvent(ownerid, name, date, location, time)
	self.response.write('Event saved successfully!')

class ViewEvent(webapp2.RequestHandler):
	def get(self):
		eventid = self.request.get('eventid')
		if(
		template_values = {
			'user': user,
		}
		template = JINJA_ENVIRONMENT.get_template('path/to/template')
		self.response.write(template.rendered(template_values))

class EditEvent(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'user': user,
		}
		template = JINJA_ENVIRONMENT.get_template('path/to/template')
		self.response.write(template.rendered(template_values))
        
app = webapp2.WSGIApplication([    
    ('/event/edit', EditEvent),  
    ('/event/view', ViewEvent),  
    ('/event/submit', SubmitEvent)
    ], debug=True)
