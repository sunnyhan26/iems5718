from datetime import datetime
import logging

timeformat="%Y-%m-%d %H:%M"

def str2datetime(timestr):
	try:
		t = datetime.strptime(timestr, timeformat)
	except ValueError:
		logging.warn("Received time with invalid format " + timestr)
		t = None
	return t

def datetime2str(datetime):
	try:
		str = datetime.strftime(timeformat)
	except AttributeError:
		str = None
	return str

def isToday(inputdate):
	return (inputdate.date() == datetime.today().date())
	
