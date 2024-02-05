import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from config import me, password

def SendMail(ImgFileName, email):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = "Билет на Рок-Концерт"
    msg['From'] = me
    msg['To'] = email

    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, password)
    s.sendmail(me, email, msg.as_string())
    s.quit()
    print("SANDED!")
