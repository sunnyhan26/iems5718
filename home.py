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

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		logoutlink = users.create_logout_url('/')
		userlist = user_func.getUserList()
		eventlist = event_func.getEventList()
		template_values = {
			'logoutlink' : logoutlink,
			'userlist' : userlist,
			'user' : user,
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/mainPage.html')
		self.response.write(template.render(template_values))

class JoinedEventPage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		eventlist = event_func.getEventListByOwner(user.user_id())
		template_values = {
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/joined.html')
		self.response.write(template.render(template_values))

class MyEventPage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		eventlist = event_func.getEventListByOwner(user.user_id())
		template_values = {
			'user' : user,
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/myEvent.html')
		self.response.write(template.render(template_values))

        
app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/home', HomePage),
    ('/home/joinedeventlist', JoinedEventPage),
    ('/home/myeventlist', MyEventPage)
    ], debug=False)
