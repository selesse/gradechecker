# grade checker composed of the following functions
#   check_minerva()
#   compare_grades()
#   prep_mail()
#   mail(course, friends, grade)

def check_minerva():
  try:
    import mechanize, random, re, time

    with open(".settings", "r") as settings:
      lines = [x.rstrip() for x in settings.readlines()]
      log_file = lines[0]
      student_id = lines[1]
      password = lines[2]

    # start the browser
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)

    br.open('https://banweb.mcgill.ca/pban1/twbkwbis.P_WWWLogin')

    br.select_form(name='loginform')

    br.form['sid'] = student_id
    br.form['PIN'] = password

    br.method="POST"
    br.submit()

    print 'Logging in...'
    time.sleep(random.uniform(1,3))

    br.follow_link(text="Student Menu", nr=0)
    time.sleep(random.uniform(1,3))

    br.follow_link(text="Student Records Menu", nr=0)
    print 'Navigating to "Student Records Menu"...'
    time.sleep(random.uniform(1,3))

    br.follow_link(text="View Your Unofficial Transcript", nr=0)
    print 'Navigating to transcript...'
    time.sleep(random.uniform(1,3))

    print 'Reading html...'
    html = br.response().read()

    grades = re.findall('fieldmediumtext>([^<]*)</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>[1-5]</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault">&nbsp;</TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>([A-Z][+-]?)</SPAN>', html)

    with open ("current_grades.txt", "w") as file:
      output = ""
      for value in grades:
        output = output + value[0] + ":" + value[1] + "|"

      file.write(output)
  except:
    print "Exception!"
    with open (log_file, "a") as log_output_file:
      log_output_file.write(" -> error checking Minerva\n")
      import traceback, sys
      traceback.print_exc(file=log_output_file)
      log_output_file.close()


def compare_grades():
  new = open("current_grades.txt", "r")
  old = open("old_grades.txt", "r")
  contents_new = new.read().split("|")[:-1]
  contents_old = old.read().split("|")[:-1]
  new.close()
  old.close()
  diff = list(set(contents_new) - set(contents_old))
  print diff

  if diff:
    prep_mail(diff)
    import shutil
    shutil.copyfile("current_grades.txt", "old_grades.txt")


def prep_mail(diff):
  with open(".friends", "r") as fp:
    friends = dict(s.strip().split(":") for s in fp.readlines())
  with open(".courses", "r") as fp:
    courses = dict([(c, f.split(',')) for c, f in [s.strip().split("|") for s in fp.readlines()]])

  for course in diff:
    course, grade = course.split(":")
  if course in courses:
    mail(course, [friends[f] for f in courses[course]], grade)

def mail(course, friends, grade):
  from gmailer import gmailer

  message = '''Hey
I'm here to report that a new grade was posted on Minerva for '''
  message += '"%s".' % course
  message += '''Go check it out if you're interested in seeing how you did.

Cheers,
Minerva Bot'''

  with open(".settings", "r") as settings:
    lines = [x.rstrip() for x in settings.readlines()]
    smtp_login = lines[3]
    smtp_password = lines[4]

  gmail = gmailer(smtp_login, smtp_password, "Minerva Bot")
  gmail.send_mail(friends, "[Minerva Grade Checker] " + course, message)

if __name__ == "__main__":
  # check grades
  #check_minerva()
  compare_grades()
