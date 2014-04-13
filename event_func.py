from google.appengine.ext import ndb    
import logging
from time_func import str2datetime, datetime2str

class Event(ndb.Model):
	ownerid = ndb.StringProperty()
	name = ndb.StringProperty()
	summary = ndb.TextProperty()
	my1Time = ndb.DateTimeProperty()
	my2Time = ndb.DateTimeProperty()
	my3Time = ndb.DateTimeProperty()
	location = ndb.StringProperty()
	lagitude = ndb.FloatProperty()
	longitude = ndb.FloatProperty()
	createTime = ndb.DateTimeProperty(auto_now_add=True)
	lastModifiedTime = ndb.DateTimeProperty(auto_now=True)


def permitted():
	return True

def addEvent(ownerid, name, summary, my1Time, my2Time, my3Time, location,
	lagitude, longitude, eventid):
	if permitted():
		# how to verify it is really a eventid?
		if eventid == '':
			mykey=None
		else:
			mykey=ndb.Key('Event', int(eventid))
		event = Event(ownerid=ownerid, name=name, summary=summary,
			my1Time=str2datetime(my1Time), my2Time=str2datetime(my2Time),
			my3Time=str2datetime(my3Time), location=location,
			lagitude=lagitude, longitude=longitude, key=mykey)
		key = event.put()
		logging.info('Event added with key %s' % key)

def getEvent(event_id):
	eventkey = ndb.Key('Event', event_id)
	event = eventkey.get()
	return event

def _fetchEventList(query):
	result = query.fetch()
	eventlist = []
	for event in result:
		eventlist.append([event.name, event.location,
			datetime2str(event.my1Time), event.key])
		logging.info(event)
	return eventlist

def getEventList():
	"""
	Return a list of event in the format of [name, location, time]
	"""
	query = Event.query()
	return _fetchEventList(query)

def getEventListByOwner(ownerUserID):
	"""
	Return a list of event created by the user with ownerUserID
	"""
	query = Event.query(Event.ownerid==ownerUserID)
	return _fetchEventList(query)
