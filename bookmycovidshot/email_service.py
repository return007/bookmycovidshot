
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Thank you for registration. We will update you once slots are available"
 
 
def send_email(email): 
    password = ""
    msg['From'] = ""
    msg['To'] = email
    msg['Subject'] = "Registration for Covid"
    
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('localhost')
    
    server.starttls()
    
    # Login Credentials for sending th`e mail
    server.login(msg['From'], password)
    
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()
    
    
