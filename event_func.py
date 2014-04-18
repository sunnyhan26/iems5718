from google.appengine.ext import ndb    
import logging
from user_func import getUserInfo
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

class EventVote(ndb.Model):
	userid = ndb.StringProperty()
	my1Vote = ndb.IntegerProperty()
	my2Vote = ndb.IntegerProperty()
	my3Vote = ndb.IntegerProperty()

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

def voteEvent(eventid, userid, voteList):
	parentkey = ndb.Key('Event', int(eventid))

	vote = EventVote(key=ndb.Key('Event', int(eventid), 'EventVote',userid),
		userid=userid,
		my1Vote=voteList[0], my2Vote=voteList[1], my3Vote=voteList[2])

	key = vote.put()
	logging.info("voted Event with key %s" %key)

def getVoteList(eventid, userid):
	ancestor_key = ndb.Key('Event', eventid)
	if userid:
		query = EventVote.query( EventVote.userid == userid,
			ancestor=ancestor_key )
	else:
		query = EventVote.query(ancestor=ancestor_key)
	result = query.fetch()
	votelist = [0, 0, 0]
	for vote in result:
		if vote.my1Vote:
			votelist[0] += 1
		if vote.my2Vote:
			votelist[1] += 1
		if vote.my3Vote:
			votelist[2] += 1
	logging.info('votelist = %s' % votelist)
	return votelist
	


def getEvent(event_id):
	eventkey = ndb.Key('Event', event_id)
	event = eventkey.get()
	logging.info('Got an event with key %d, %s' % (event_id, event))
	return event

def _fetchEventList(query):
	result = query.fetch()
	eventlist = []
	for event in result:
		eventlist.append([event.name, event.location,
			datetime2str(event.my1Time), event.key.id()])
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

def getEventListByVoter(voterUserID):
	"""
	Return a list of event a user has voted
	"""
	query = EventVote.query(EventVote.userid==voterUserID)
	result = query.fetch()
	eventlist = []
	for eventvote in result:
		event = eventvote.key.parent().get()
		eventlist.append([event.name, event.location,
			datetime2str(event.my1Time), event.key.id()])
		logging.info(event)
	return eventlist

def getJoinedUserList(eventid):
	"""
	Return a list of joined user
	"""
	userlist = []
	ancestor_key = ndb.Key('Event', eventid)
	query = EventVote.query(ancestor=ancestor_key)
	result = query.fetch()
	for vote in result:
		userlist.append(getUserInfo(vote.userid))
	return userlist
