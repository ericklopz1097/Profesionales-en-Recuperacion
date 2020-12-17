import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

def send_mail(send_from: str,subject: str, text: str, send_to: list, files=None):
    
    send_to = default_adress if not sent_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in file or []:
        with open(f, 'rb') as fil:
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(),_subtype=ext)
            attachedfile.add_header('content-disposition', 'attachment', filename=basename(f))
            msg.attach(attachedfile)
    
    smtp = smtplib.SMTP(host='', port=3301)
    smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(send_from,send_to,msg.as_string())
    smtp.close()

