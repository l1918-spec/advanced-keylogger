# KeyLogger Project

A Python-based keylogger project that captures keystrokes, system information, clipboard data, audio recordings, and screenshots. The project can also send collected data to a specified email address. Encrypted data files are stored locally and can be decrypted with a generated key.

## Features

- **Keystroke Logging**: Records all keystrokes and saves them to a file.
- **System Information Logging**: Captures information about the operating system, IP address, and machine details.
- **Clipboard Data Logging**: Copies the clipboard contents and stores them locally.
- **Audio Recording**: Records audio from the microphone for a specified duration.
- **Screenshot Capture**: Takes screenshots of the screen.
- **Email Sending**: Sends collected logs to a specified email address.
- **Encryption**: Encrypts the collected data files using a unique key for security.
- **Decryption**: Decrypts encrypted files for reviewing the collected information.

## Prerequisites

- Python 3.6+
- Required libraries:
  - `cryptography`
  - `pynput`
  - `scipy`
  - `pillow`
  - `sounddevice`
  - `requests`
  - `win32clipboard` (Windows only)





---

This README provides a clear overview of the project, setup instructions, and usage guidelines. Make sure to replace placeholders like email credentials and adjust configurations as needed before using or sharing the project.


## configuration email setup :
-*email_address = "your_email@gmail.com"*
-*password = "your_email_password"*
-*toaddr = "recipient_email@gmail.com"*


## Contributing : 
-**If you see ways to improve the project, feel free to fork the repository and submit a pull request with your ideas or fixes! Contributions to make this project better are always welcome.**




