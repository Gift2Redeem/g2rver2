import smtplib
from django.conf import settings


def send_email(to, subject, text):
	import pdb;pdb.set_trace()
	FROM = "sender@example.com"

	# Prepare actual message

	message = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (FROM, ", ".join(to), subject, text)

	# Send the mail

	server = smtplib.SMTP("Mail.yahoo.com")
	server.sendmail(FROM, to, message)
	server.quit()


def send_sms(mob, message):
    """
Function for sms sending
Params @mob = list of mobile numbers ex : ["919999912345","447777712345","18888812345"]
@message = Message which send ex: "Your otp is :5432323"
"""
    try:
        import zensend
        client = zensend.Client(settings.SMS_API_AUTH_CODE)
        result = client.send_sms(body = message, originator = "G2R", numbers = mob)
        return True
    except:
        print "No sms sending"
        return False

def send_mail2(toaddr, subject, body):
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEText import MIMEText
	 
	 
	fromaddr = settings.MAIL_USERNAME
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject 
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP(settings.MAIL_SERVER)
	server.starttls()
	server.login(fromaddr, settings.MAIL_PASSWORD)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()