from email.header import decode_header
from bs4 import BeautifulSoup
import smtplib
import imaplib
import email
import re


class EmailOperations:
    
    def __init__(self,email,password):

        self.emailAddress = email
        self.emailPassword = password
        self.emailProvider = email.split("@")[1]
        self.latestMailId = None
    
    def set_emailAddress(self, email):
        self.emailAddress = email
    
    def set_emailPassword(self, password):
        self.emailPassword = password

    def send(self,recipient,subject,body):
        try:
            with smtplib.SMTP_SSL('smtp.'+self.emailProvider, 465) as smtp:

                smtp.login(self.emailAddress, self.emailPassword)
                msg = f'Subject: {subject}\n\n{body}'
                smtp.sendmail(self.emailAddress,recipient, msg)
                return "Email sent"
        except Exception as e:
            return "Couldn't send email "+str(e)
    
    def get_body(self,msg):
        if msg.is_multipart():
            return self.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)
    
    def replace(self, string, regex, replaceWith):
        string = re.sub(regex, replaceWith, string)
        return string

    def fetch(self,fetchCount):
        try:
            with imaplib.IMAP4_SSL('imap.'+self.emailProvider) as imap:
                imap.login(self.emailAddress,self.emailPassword)
                status, messages = imap.select('INBOX')
                messages = messages[0]

                for i in range(fetchCount):
                    messages = bytes(str(int(messages)-i),"utf-8")

                    status, data = imap.fetch(messages, "(RFC822)")
                    data = data[0][1]

                    rawMsg = email.message_from_bytes(data)
                    subject = rawMsg["subject"]
                    sender = rawMsg["from"]

                    body = self.get_body(rawMsg).decode("utf-8")
                    body = BeautifulSoup(body, "html.parser").get_text()
                    body = self.replace(body, r"http\S+","Link.")   #Replaces all links.
                    body = self.replace(body, r"\r|\n","")  #Replaces all backslash characters.

                    yield sender, subject, body
        except Exception as e:
            return "Couldn't fetch email "+str(e)

    #Checks for new emails
    def check(self):
        try:
            with imaplib.IMAP4_SSL('imap.'+self.emailProvider) as imap:
                imap.login(self.emailAddress,self.emailPassword)
                # print(imap.list())
                status, message = imap.select('INBOX', readonly = True)
                # print(message)
                result, data = imap.uid("search", None, "ALL")
                # print(data)
                idList = data[0].split()
                # print(idList)

                if self.latestMailId == None:
                        self.latestMailId = idList[-1]

                mailCount = len(idList) - idList.index(self.latestMailId) - 1
                # print(mailCount)
                self.latestMailId = idList[-1]
                
                return mailCount
        except Exception as e:
            return 0
            

    def delete(self,emailId):
        pass
