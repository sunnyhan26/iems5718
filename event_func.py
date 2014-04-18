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
	cancelled = ndb.BooleanProperty()
	createTime = ndb.DateTimeProperty(auto_now_add=True)
	lastModifiedTime = ndb.DateTimeProperty(auto_now=True)

class EventVote(ndb.Model):
	userid = ndb.StringProperty()
	my1Vote = ndb.IntegerProperty()
	my2Vote = ndb.IntegerProperty()
	my3Vote = ndb.IntegerProperty()
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
			lagitude=lagitude, longitude=longitude, cancelled=False, key=mykey)
		key = event.put()
		logging.info('Event added with key %s' % key)

def cancelEvent(eventid):
	if permitted():
		event = getEvent(int(eventid))
		event.cancelled = True
		event.put()

def voteEvent(eventid, userid, voteList):
	parentkey = ndb.Key('Event', int(eventid))

	vote = EventVote(key=ndb.Key('Event', int(eventid), 'EventVote',userid),
		userid=userid,
		my1Vote=voteList[0], my2Vote=voteList[1], my3Vote=voteList[2])

	key = vote.put()
	logging.info("voted Event with key %s" %key)

def getVoteNoList(eventid, userid):
	"""
	Return a list of number of vote of a particular event
	If userid is not set, all votes for the event are counted
	Otherwise, only the event of the user is counted
	"""
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
	
def getVoteList(eventid):
	"""
	Return all the EventVote of the event
	"""
	ancestor_key = ndb.Key('Event', eventid)
	query = EventVote.query(ancestor=ancestor_key)
	result = query.fetch()
	return result


def getEvent(event_id):
	eventkey = ndb.Key('Event', event_id)
	event = eventkey.get()
	return event

def _fetchEventList(query):
	result = query.fetch()
	eventlist = []
	for event in result:
		eventlist.append([event.name, event.location,
			datetime2str(event.my1Time), event.key.id(), event.cancelled])
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
			datetime2str(event.my1Time), event.key.id(), event.cancelled])
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

def isEventUdpatedToday(eventid):
	"""
	Check whether the event it updated today
	Return a Boolean list
	which, if true, indicates the event was upated, new comments were
	added and new votes were added respectively
	"""
	event=getEvent(int(eventid))
	eventupdated = isToday(event.lastModifiedTime)

	commentlist = getCommentList(eventid)
	commentupdated = False
	for comment in commentlist:
		if isToday(str2datetime(comment[2])):
			commentupdated = True
	
	votelist = getVoteNoList(int(eventid))
	voteupdated = False
	for vote in votelist:
		if isToday(vote.lastModifiedTime):
			voteupdated = True

	return [eventupdated, commentupdated, voteupdated]



