from google.appengine.ext import ndb    
import logging

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
			event = Event(ownerid=ownerid, name=name, summary=summary,
				my1Time=my1Time,
				my2Time=my2Time, my3Time=my3Time, location=location,
				lagitude=lagitude, longitude=longitude)
		else:
			mykey=ndb.Key('Event', eventid)
			event = Event(ownerid=ownerid, name=name, summary=summary,
				my1Time=my1Time,
				my2Time=my2Time, my3Time=my3Time, location=location,
				lagitude=lagitude, longitude=longitude, key=mykey)
		key = event.put()
		logging.info('Event added with key %s' % key)

def getEvent(event_id):
	eventkey = ndb.Key('Event', event_id)
	event = eventkey.get()
	return event

def getEventList():
	"""
	Return a list of event in the format of [name, location, time]
	"""
	eventlist = []
	query = Event.query()
	result = query.fetch()
	for event in result:
		eventlist.append([event.name, event.location, event.my1Time])
		logging.info(event)
	return eventlist
