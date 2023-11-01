import os
import glob
import picamera
import RPi.GPIO as GPIO
import smtplib
from time import sleep
import webbrowser
import pyautogui
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# Important variables:
sender = 'sender@outlook.com'
password = '***********'
receiver = 'receiver@gmail.com'
BUTTON_PIN=16
DIR = './Visitors/'
prefix = 'image'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)

def video_call():
    url='https://meet.jit.si/someRandomCall'
    webbrowser.open(url)
    sleep(5)
    pyautogui.press('enter')
    sleep(60)
    os.system("taskkill /f /im chrome.exe")

def send_mail(filename):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Visitor'
    body = 'You have a visitor in the house. Check them out here:https://meet.jit.si/someRandomCall'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()

def capture_img():
    print('capturing')
    if not os.path.exists(DIR):
    os.makedirs(DIR)
    files = sorted(glob.glob(os.path.join(DIR, prefix + '[0-9][0-9][0-9].jpg')))
    count = 0
    if len(files) > 0:
        count = int(files[-1][-7:-4])+1
    filename = os.path.join(DIR, prefix + '%03d.jpg' % count)
    with picamera.PiCamera() as camera:
    pic = camera.capture(filename)
    send_mail(filename)
    video_call()

try:
    while True:
    if GPIO.input(BUTTON_PIN)==GPIO.LOW:
        capture_img()
except KeyboardInterrupt:
    GPIO.cleanup()