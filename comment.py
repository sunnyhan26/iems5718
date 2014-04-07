import webapp2
import comment_func
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

class AddComment(webapp2.RequestHandler):
	def post(self):
		eventid = self.request.get('eventid')
		comment = self.request.get('comment')

		logging.info('Received AddComment for ' + eventid + ' : ' + comment)

		addComment(eventid, comment)

class GetList(webapp2.RequestHandler):
	def post(self):
		eventid = self.request.get('eventid')
		startcomment = self.request.get('startcomment')
		commentno = self.request.get('commentno')

		logging.info('Received GetList for ' + eventid + ', startcomment' + 
			startcomment +', no: ' + commentno)

		commentlist = getCommentList()



app = webapp2.WSGIApplication([    
    ('/comments/add', AddComment),  
    ('/comments/getlist', GetList)
    ], debug=True)
