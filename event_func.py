from google.appengine.ext import ndb    

class Event(ndb.Model):
	ownerid = ndb.StringProperty()
	name = ndb.StringProperty()
	my1Time = ndb.DateTimeProperty()
	my2Time = ndb.DateTimeProperty()
	my3Time = ndb.DateTimeProperty()
	location = ndb.StringProperty()
	coordinate = ndb.GeoPtProperty()

def permitted():
	return

def addEvent(ownerid, name, my1Time, my2Time, my3Time, location,
	coordinate, eventid):
	if permitted():
		# how to verify it is really a eventid?
		if eventid is None:
			event = Event(ownerid=ownerid, name=name, my1Time=my1Time,
				my2Time=my2Time, my3Time=my3Time, location=location,
				coordinate=coordinate)
		else:
			mykey=Key('Event', eventid)
			event = Event(ownerid=ownerid, name=name, my1Time=my1Time,
				my2Time=my2Time, my3Time=my3Time, location=location,
				coordinate=coordinate, key=mykey)
		event.put()

def getEvent(event_id):
	eventkey = ndb.Key('Event', event_id)
	event = eventkey.get()
	return event

def getEventList():
	query = Event.all()
	eventlist = query.fetch()
	return eventlist
