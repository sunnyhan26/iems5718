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

def getuserlist():
	userlist = ['user0',
		'user1',
		'user2',
		'user3',
		'user4',
		'user5',
		'user6',
		'user7',
		'user8',
		'user9',
		'usera']
	return userlist

def geteventlist():
	eventlist = [
		['event0', 'location0', 'time0'],
		['event1', 'location1', 'time1'],
		['event2', 'location2', 'time2'],
		['event3', 'location3', 'time3'],
		['event4', 'location4', 'time4'],
		['event5', 'location5', 'time5'],
		['event6', 'location6', 'time6'],
		['event7', 'location7', 'time7'],
		['event8', 'location8', 'time8'],
		['event9', 'location9', 'time9'],
		['event10', 'location10', 'time10']
		]
	return eventlist

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		logoutlink = users.create_logout_url('/')
		userlist = user_func.getUserList()
		eventlist = geteventlist()
		template_values = {
			'logoutlink' : logoutlink,
			'userlist' : userlist,
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/mainPage.html')
		self.response.write(template.render(template_values))

class JoinedEventPage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		eventlist = geteventlist()
		template_values = {
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/joined.html')
		self.response.write(template.render(template_values))

class MyEventPage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser(self)
		eventlist = geteventlist()
		template_values = {
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/myEvent.html')
		self.response.write(template.render(template_values))

        
app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/home', HomePage),
    ('/home/joinedeventlist', JoinedEventPage),
    ('/home/myeventlist', MyEventPage)
    ], debug=True)
