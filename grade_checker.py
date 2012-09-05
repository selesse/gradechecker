import mechanize
import time
import random

date = time.localtime()
months = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")
year = date[0]
month = months[date[1]-1]
dayofmonth = date[2]
hour = date[3]
minute = date[4]
second = date[5]

def check_minerva():
  try:
    # start the browser
    br=mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)

    br.open('https://banweb.mcgill.ca/pban1/twbkwbis.P_WWWLogin')

    br.select_form(name='loginform')

    br.form['sid'] = "student id"
    br.form['PIN'] = "pin"

    br.method="POST"
    br.submit()

    print 'logging in...'
    time.sleep(random.uniform(1,2))

    br.follow_link(text="Student Menu", nr=0)
    time.sleep(random.uniform(1,2))

    br.follow_link(text="Student Records Menu", nr=0)
    print 'navigating to records menu...'
    time.sleep(random.uniform(1,2))

    br.follow_link(text="View Your Unofficial Transcript", nr=0)
    print 'navigating to transcript...'
    time.sleep(random.uniform(1,2))

    print 'reading html...'
    html = br.response().read()

    import re
    grades = re.findall('fieldmediumtext>([^<]*)</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>[1-5]</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault">&nbsp;</TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>([A-Z][+-]?)</SPAN>', html)

    with open ("grades.txt", "w") as file:
      output = ""
      for value in grades:
        output = output + value[0] + ":" + value[1] + "|"

      file.write(output)

    logFile = open ("/home/alex/.logs/gradechecker.log", "a")
    dateAndTime = "%s %d %d, %2d:%02d:%02d %2s" % (month, dayOfMonth, year, 12 if hour%12==0 else hour%12, minute, second, "AM" if hour < 12 else "PM")
    logFile.write(dateAndTime + " -> checked Minerva\n")
    logFile.close()
  except:
    logFile = open ("/home/alex/.logs/gradechecker.log", "a")
    dateAndTime = "%s %d %d, %2d:%02d:%02d %2s" % (month, dayOfMonth, year, hour%12 if hour > 0 else 12, minute, second, "AM" if hour < 12 else "PM")
    logFile.write(dateAndTime + " -> error checking Minerva\n")
    import traceback, sys
    traceback.print_exc(file=logFile)
    logFile.close()


def compareGrades():
  new = open("grades.txt", "r")
  old = open("currentGrades.txt", "r")
  contents_new = new.read().split("|")[:-1]
  contents_old = old.read().split("|")[:-1]
  new.close()
  old.close()
  diff = list(set(contents_new) - set(contents_old))
  print diff

  if diff:
    prep_mail(diff)
    import shutil
    shutil.copyfile("grades.txt", "currentGrades.txt")


def prep_mail(diff):
  with open("friends", "r") as fp:
    friends = dict(s.strip().split(":") for s in fp.readlines())
  with open("courses", "r") as fp:
    courses = dict([(c, f.split(',')) for c, f in [s.strip().split("|") for s in fp.readlines()]])

  for course in diff:
    course, grade = course.split(":")
  if course in courses:
    mail(course, [friends[f] for f in courses[course]], grade)

def mail(course, friends, grade):
  print "hi"

if __name__ == "__main__":
  # check grades
  check_minerva()
