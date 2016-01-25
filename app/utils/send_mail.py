import smtplib
from django.conf import settings


def send_email(to, subject, text):
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


def send_zensend(mob, message):
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

def send_sms_msg91(mob, message):
	try:

		import urllib # Python URL functions
		import urllib2 # Python URL functions

		authkey = "102986AgpB0V2tLD56a5bd22" # Your authentication key.

		mobiles = mob # Multiple mobiles numbers separated by comma.

		message = message # Your message to send.

		sender = "NUTECH" # Sender ID,While using route4 sender id should be 6 characters long.

		route =  4 # Define route

		# Prepare you post parameters
		values = {
		          'authkey' : authkey,
		          'mobiles' : mobiles,
		          'message' : message,
		          'sender' : sender,
		          'route' : route,
		          'country' : 0
		          }


		url = "http://api.msg91.com/api/sendhttp.php" # API URL

		postdata = urllib.urlencode(values) # URL encoding the data here.

		req = urllib2.Request(url, postdata)

		response = urllib2.urlopen(req)

		output = response.read() # Get Response
		return True
	except:
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

def twilo_sms():
	from twilio.rest import TwilioRestClient 
 
	# put your own credentials here 
	ACCOUNT_SID = "AC5ef872f6da5a21de157d80997a64bd33" 
	AUTH_TOKEN = "[AuthToken]" 
	 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
	    to="+16518675309", 
	    from_="+14158141829", 
	    body="Hey Jenny! Good luck on the bar exam!", 
	    media_url="http://farm2.static.flickr.com/1075/1404618563_3ed9a44a3a.jpg", 
	)