from google.appengine.ext import ndb    

class Event(ndb.Model):
	ownerid = ndb.StringProperty()
	name = ndb.StringProperty()
	location = ndb.GeoPtProperty()
	time = ndb.DateProperty()

def permitted():
	return

def addEvent(eventid, ownerid, name, location, time):
	if permitted():
		# how to verify it is really a eventid?
		if eventid is NULL:
			event = Event(ownerid=ownerid, name=name, location=location,
				time=time)
		else:
			event = Event(key=Key('Event', eventid), ownerid=ownerid,
				name=name, location=location, time=time)
		event.put()

def getEvent(event_id):
	eventkey = ndb.Key('Event', event_id)
	event = eventkey.get()
	return event

def getEventList():
	query = Event.all()
	eventlist = query.fetch()
	return eventlist
