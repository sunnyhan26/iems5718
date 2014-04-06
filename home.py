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

class HomePage(webapp2.RequestHandler):
	def get(self):
		template_values = {
		}
		template = JINJA_ENVIRONMENT.get_template('/template/Web_project.html')
		self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([
    ('/home', HomePage),
    ('/home/joinedeventlist', HomePage),
    ('/home/myeventlist', HomePage)
    ], debug=True)
