import webapp2
from google.appengine.api import users
import event_func
import user_func
from google.appengine.api import mail
import logging

senderemail="sunnuyhan26@gmail.com"
projectid="organic-diode-554"

def sendImmediateEmail(eventid,eventname):
	logging.info("email test")
        userlist=event_func.getJoinedUserList(int(eventid))
        logging.info("sajnfewkfnw"+str(len(userlist)))
        for item in userlist:
            useremail=item.email
            message = mail.EmailMessage(sender=senderemail,
                            subject="Your account has been approved")

            message.to = useremail
            message.body = """
Dear """+ item.name + """:
The event owner has finalized the event--"""+eventname+""". Please check by the following link and attend the event in time.
"""+ """http://"""+projectid+""".appspot.com/event/view?eventid="""+str(eid)+"""

Enjoy the event and have a good time.

Group13 Team
"""
            message.send()
        #self.response.write("The event will be informed to all participants by email")



'''every item of updatelist is [eventid, eventname, [event update, new comment, new vote, cancelled]]'''
def sendEmail(updatelist):
    '''collect the update, create sendcontent'''
    updatecontent=["event update","new comment","new vote","cancelled"]
    sendcontent="""Some event update informations are lsited below:
    
"""
    for item in updatelist:
        if item[2]!=[0,0,0,0]:
            count=1
            sendcontent=sendcontent+"""Event: """+item[1]+""" has """
            for index in range(len(item[2])):
                if item[2][index]==1:
                    sendcontent=sendcontent+str(count)+""". """+updatecontent[index]
                    count=count+1
            sendcontent=sendcontent+"""
Please click the link http://"""+projectid+""".appspot.com/event/view?eventid="""+item[0]+""" to see details.
            
"""
     
            
    """send email to all """
    #userlist=event_func.getJoinedUserList(int(eventid))
    userlist=user_func.getUserList()
    logging.info("sajnfewkfnw"+str(userlist[0].email))
    for item in userlist:
        useremail=item.email
        message = mail.EmailMessage(sender=senderemail,
                            subject="Event Update Information Form Group13")

        message.to = useremail
        message.body = """
Dear """+ item.name +""" :
"""+sendcontent+"""
            
Please let us know if you have any questions.

Group13 Team
"""
        message.send()




	
