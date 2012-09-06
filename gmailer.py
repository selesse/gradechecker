class gmailer:
  def __init__(self, smtp_login, smtp_password, email_from):
    import smtplib

    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()
    smtp_obj.login(smtp_login, smtp_password)

    if len(email_from) == 0:
      email_from = smtp_login[0:smtp_login.find("@")]

    self.smtp_obj = smtp_obj
    self.email_from = email_from
    self.smtp_login = smtp_login
    self.smtp_password = smtp_password

  def send_mail(self, recipients, subject, message):
    if not isinstance(recipients, list):
      recipients = [recipients]

    msg = 'To: %s\n' % ",".join(recipients)
    msg += 'From: %s\n' % self.smtp_login
    msg += 'Subject: %s\n' % subject
    msg += '\n'
    msg += message

    print msg

    self.smtp_obj.sendmail(self.email_from, recipients, msg)
