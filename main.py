from assistant import Assistant
from email_operations import EmailOperations
from time import sleep
import threading


#Enter your email and password
emailId = ""
password = ""

a = Assistant(None, 150)
print("Assistant object created")
e = EmailOperations(emailId, password)
print("Email object Created")

greetings = "Hello, Welcome to Email Service for blinds, This is your assistant."

instructions = """
                Take a second to respond after i speak.
                I can't hear properly, so, be loud and clear otherwise your voice won't be recognised.
                You can give me any name and i will respond only to that.
                You can always say help to know these instructions anytime in the future.
                Say command to know all the commands.
                Email alerts are on by default.
                
                I am not a smart assistant, so, speak only what's important.
                Thank you.
                """

commands = """
            The following are the commands:

            Send - to send an email to anyone.
            Fetch - to fetch emails from your inbox.
            Instructions - to know instructions.
            Alert - put alerts to mute/unmute.
            Stop - to stop using this service.
            """


def check_mails(assistant, email, interval):

    while True:
        newMails = email.check()
        if newMails > 0:
            if alerts == True:
                assistant.speak("You have "+str(newMails)+" new email")
        sleep(interval)

def send():
    print("Send function called")
    to = a.listen("Say recipient's name, only before the at the rate symbol").lower().replace(" ","")
    print("Email to : ",to)
    mailProvider = a.listen("Say recipient's mail provider").lower().replace(" ","")
    print("Email provider : ",mailProvider)
    subject = a.listen("Say subject of email")
    print("Subject : ",subject)
    body = a.listen("Say body of email")
    print("Body : ",body)

    e.send(to+"@"+mailProvider+".com", subject, body)

def read():
    print("Read function called")
    try:
        fetchCount = int(a.listen("How many emails should i fetch?"))
    except Exception as ex:
        fetchCount = 1
        print(ex)
    a.speak(f"Fetching {fetchCount} email.")
    print(f"Fetching {fetchCount} email.")
    for sender, subject, body in e.fetch(fetchCount):
        print("Email : \n", sender, "\n", subject, "\n", body)

        a.speak("New Email")
        a.speak(f"From : {sender}")
        a.speak(f"Subject : {subject}")
        a.speak(f"Body : {body}")


def main():
    a.speak(greetings)
    a.speak(instructions)
    a.speak(commands)

    name = ""
    while name == "":
        a.speak("What would you like to name me")
        name = a.listen()
    a.set_name(name)
    print("Assistant named to : ",a.get_name())

    a.speak("You may start using the service now, by saying "+name)

    #always listening
    stopper = a.listen_constantly()

    #new thread to start the email alert process
    emailAlertThread = threading.Thread(target = check_mails, kwargs = dict(assistant = a, email = e, interval = 10))
    emailAlertThread.daemon = True
    emailAlertThread.start()
    global alerts
    alerts = True

    service = True
    while service:
        recognized_audio = a.get_recognized_audio()

        if recognized_audio not in ("", None) and recognized_audio.split()[-1] == name:

            a.set_recognized_audio(None)

            command = a.listen("Listening")
            print("Command : ",command)

            if command.lower() == "send":
                send()
            
            elif command.lower() in  ("fetch", "patch", "search","read"):
                read()
            
            elif command.lower() in ("help", "instruction", "instructions"):
                a.speak(instructions)
            
            elif command.lower() in ("command", "commands"):
                a.speak(commands)
            
            elif command.lower() in ("alert", "alerts"):
                if alerts:
                    alerts = False
                    a.speak("Alerts are on.")
                else:
                    alerts = True
                    a.speak("Alerts are off.")
            
            elif command.lower() == "stop":
                print("\nUser asked to stop the service")
                stopper()
                service =False
            
            else:
                a.speak("Command not recognized")

main()

print("Service stopped")
print("Made by : Prabhat")

sleep(2)
