from google.appengine.ext import ndb    
import logging
from user_func import getUserInfo
from time_func import str2datetime, datetime2str, getTimeNow, isToday
from comment_func import getCommentList

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
	cancelTime = ndb.DateTimeProperty()
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
			event = Event()
			event.cancelled=False
		else:
			event = ndb.Key('Event', int(eventid)).get()
		event.ownerid = ownerid
		event.name = name
		event.summary = summary
		event.my1Time=str2datetime(my1Time)
		event.my2Time=str2datetime(my2Time)
		event.my3Time=str2datetime(my3Time)
		event.location=location
		event.lagitude=lagitude
		event.longitude=longitude
		key = event.put()
		logging.info('Event added with key %s' % key)

def cancelEvent(eventid):
	if permitted():
		event = getEvent(int(eventid))
		event.cancelled = True
		event.cancelTime = getTimeNow()
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
	Return a list of event in the format of [name, location, time, eventid, cancelled]
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
	Return None if the event was not updated
	"""
	event=getEvent(int(eventid))
	eventupdated = isToday(event.lastModifiedTime)

	commentlist = getCommentList('%d' % eventid)
	commentupdated = False
	for comment in commentlist:
		if isToday(str2datetime(comment[2])):
			commentupdated = True
	
	votelist = getVoteList(int(eventid))
	voteupdated = False
	for vote in votelist:
		if isToday(vote.lastModifiedTime):
			voteupdated = True

	if(event.cancelled):
		cancelled = isToday(event.cancelTime)
	else:
		cancelled = False

	if eventupdated or commentupdated or voteupdated or cancelled: 
		return [eventupdated, commentupdated, voteupdated, cancelled]
	else:
		return None

def isEventListUpdatedToday(eventlist):
	"""
	Check whether the list of event is updated
	Return a list of updated event in this format:
	[ eventid, eventname, [eventUpdated, CommentUpdated, voteUpdated, cancelled] ]
	"""
	updatedEventList = []
	for event in eventlist:
		updatelist = isEventUdpatedToday(event[3])
		if updatelist:
			updatedEventList.append([event[3], event[0], updatelist])
	return updatedEventList

def getUpdatedEventListByOwner(ownerUserID):
	"""
	Get a list of updated event by owner
	The return format is the same as isEventListUpdatedToday
	"""
	eventlist = getEventListByOwner(ownerUserID)
	updatedlist = isEventListUpdatedToday(eventlist)
	return updatedlist

def getUpdatedEventListByVoter(voterUserID):
	"""
	Get a list of updated event by voter 
	The return format is the same as isEventListUpdatedToday
	"""
	eventlist = getEventListByVoter(voterUserID)
	return isEventListUpdatedToday(eventlist)
