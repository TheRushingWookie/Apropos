#!/usr/bin/python

import smtplib

def send_email(user, password, user_address, receiver, message):     
    # Initialize SMTP server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, password)
    
    # Send email    
    server.sendmail(user_address, receiver, message)
    server.quit()
