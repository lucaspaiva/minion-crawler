import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
	"""
	Envia email , soporta adjuntos

	"""
	msg = MIMEMultipart()
	msg['From'] = send_from
	msg['To'] = COMMASPACE.join(send_to) #multiples
	#msg['To'] = send_to #single
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach( MIMEText(text, 'html') )

	for f in files:
	    part = MIMEBase('application', "octet-stream")
	    part.set_payload( open(f,"rb").read() )
	    Encoders.encode_base64(part)
	    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
	    msg.attach(part)

	smtp = smtplib.SMTP('smtp.gmail.com:587')
	smtp.starttls()
	smtp.login('ichoteles.despegar@gmail.com','actron600')
	smtp.sendmail(send_from, send_to, msg.as_string())
	smtp.close()        