import smtplib

from api.config import Config

def send_mail(fromaddr, toaddrs, msg):
    server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(Config.MAIL_USERNAME, Config.EMAIL_HOST_PASSWORD)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


