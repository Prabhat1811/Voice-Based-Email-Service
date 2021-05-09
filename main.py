from assistant import Assistant
from email_operations import EmailOperations
from time import sleep
import threading


#enter your email and password
emailId = ""
password = ""

a = Assistant(None, 140, threshold = 550)
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

def get_credential(msg, classType):
    loop = True
    while loop:
        credential = classType(a.listen(msg).lower().replace(" ",""))
        if credential == "":
            a.speak("Try speaking something")
            continue
    
        if classType == str:
            credential = credential.lower()

        while True:
            check = a.listen(f"Do you mean {credential}?")

            if check == "yes":
                loop = False
                break
            elif check == "no":
                break
            else:
                a.speak("Not recognized")
    return credential

def send():
    print("Send function called")

    to = get_credential("Say recipient's name, only before the at the rate symbol", str)
    print("To : ",to)

    mailProvider = get_credential("Say recipient's mail provider", str)
    print("Provider : ",mailProvider)

    subject = get_credential("Say subject of email", str)
    print("Subject : ",subject)

    body = get_credential("Say body of email", str)
    print("Body : ",body)

    res = e.send(to+"@"+mailProvider+".com", subject, body)

    return res

def read():
    print("Read function called")
    
    fetchCount = get_credential("How many emails should i fetch?", int)
    a.speak(f"Fetching {fetchCount} email.")
    print(f"Fetching {fetchCount} email.")
    for sender, subject, body in e.fetch(fetchCount):
        print("Email : \n", sender, "\n", subject, "\n", body)

        a.speak("New Email")
        a.speak(f"From : {sender}")
        a.speak(f"Subject : {subject}")
        a.speak(f"Body : {body}")

    return "Reading emails finished"


def main():
    # a.speak(greetings)
    # a.speak(instructions)
    # a.speak(commands)

    name = get_credential("What would you like to name me", str)
    name = name[0].upper()+name[1:]

    a.set_name(name)
    print("Assistant named to : ",a.get_name())

    a.speak(f"You may start using the service now, by saying {name}")

    #always listening
    stopper = a.listen_constantly()

    #new thread to start the email alert process
    emailAlertThread = threading.Thread(target = check_mails, kwargs = dict(assistant = a, email = e, interval = 10))
    emailAlertThread.daemon = True
    emailAlertThread.start()

    """
    main loop
    """
    global alerts
    alerts = True
    service = True
    while service:
        recognized_audio = a.get_recognized_audio()

        if recognized_audio not in ("", None) and recognized_audio.split()[-1] == name:

            a.set_recognized_audio(None)

            command = a.listen("Listening")
            print("Command : ",command)

            if command.lower() in ("send", "spend"):
                a.speak(send())
            
            elif command.lower() in ("fetch", "patch", "search","read"):
                a.speak(read())
            
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
