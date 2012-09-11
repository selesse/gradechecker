class gmailer(object):
  def __init__(self, smtp_login, smtp_password, email_from):
    import smtplib

    # if no email-from is supplied, use the name before the @
    #   i.e. "email@example.com" becomes "email"
    if not email_from:
      email_from = smtp_login[0:smtp_login.find("@")]

    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()
    smtp_obj.login(smtp_login, smtp_password)

    self.smtp_obj = smtp_obj
    self.smtp_login = smtp_login
    self.email_from = email_from
    self.smtp_password = smtp_password

  def send_mail(self, recipients, subject, message):
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    # if recipients is not a list (i.e. single email), make it so
    if not isinstance(recipients, list):
      recipients = [recipients]

    msg = MIMEMultipart()
    msg['From'] = '"%s" %s' % (self.email_from, self.smtp_login)
    msg['To'] = ",".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    self.smtp_obj.sendmail(self.email_from, recipients, msg.as_string())
