import curses
import RPi.GPIO as GPIO
import time
from twilio.rest import Client

accountSID = 'ACb1f3f3d99e63740744add8a57c12e370'
authToken = '16a717c38d669eb433cb8f740c830ef3'
client = Client(accountSID, authToken)
twil = '+18562813693'
cell = '+12672575691'

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.IN)
old_status = GPIO.input(23)

tc = curses.initscr()
tc.nodelay(1)
tc.addstr(1, 0, "Press space to quit\n")
tc.addstr(2, 0, "")


while 1:
    kbval = tc.getch()
    status = GPIO.input(23)
    GPIO.output(22, status)
    if status != old_status:
        if status == 1:
            tc.addstr(2, 0, "DOOR IS: CLOSED")
            tc.refresh()
            message = client.messages.create(
                to=cell,
                from_=twil,
                body="The door has been closed")
            time.sleep(2)
        elif status == 0:
            tc.addstr(2, 0, "DOOR IS:   OPEN")
            tc.refresh()
            message = client.messages.create(
                to=cell,
                from_=twil,
                body="The door has been opened")
            time.sleep(2)
    old_status = status
    if kbval == 0x20:
        break

curses.endwin()
GPIO.cleanup()
print "Done"
