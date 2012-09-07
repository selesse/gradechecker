class gmailer:
  def __init__(self, smtp_login, smtp_password, email_from):
    import smtplib

    # if no email-from is supplied, use the name before the @
    #   i.e. "email@example.com" becomes "email"
    if len(email_from) == 0:
      email_from = smtp_login[0:smtp_login.find("@")]

    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()
    smtp_obj.login(smtp_login, smtp_password)

    self.smtp_obj = smtp_obj
    self.email_from = email_from
    self.smtp_login = smtp_login
    self.smtp_password = smtp_password

  def send_mail(self, recipients, subject, message):
    # if recipients is not a list (i.e. single email), make it so
    if not isinstance(recipients, list):
      recipients = [recipients]

    body = 'To: %s\n' % ",".join(recipients)
    body += 'From: %s\n' % self.smtp_login
    body += 'Subject: %s\n' % subject
    body += '\n'
    body += message

    self.smtp_obj.sendmail(self.email_from, recipients, body)
