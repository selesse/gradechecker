import mechanize, random, re, time, shutil

class grade_checker:
  @staticmethod
  def first_run():
    """First run to generate current_grades."""
    checker = grade_checker()
    (student_id, password) = checker.load_settings()
    html = checker.get_html(student_id, password)
    grades = checker.get_grades_from_html(html)
    checker.write_grades(grades)
    checker.write_grades(grades, "old_grades.txt")
    courses_without_grades = checker.get_courses_without_grades(html)
    checker.write_courses(courses_without_grades)

  def get_grades(self):
    """Get current grades from minerva, write it to current_grades."""
    (stud_id, password) = checker.load_settings()
    html = checker.get_html(stud_id, password)
    grades = checker.get_grades_from_html(html)
    checker.write_grades(grades)
    return grades

  def load_settings(self):
    """Load settings, set instance variables, return log, id and password."""
    with open(".settings", "r") as settings:
      lines = [x.rstrip() for x in settings.readlines()]
      self.student_id = lines[0]
      self.password = lines[1]
      self.smtp_login = lines[2]
      self.smtp_password = lines[3]
    return (self.student_id, self.password)

  def get_html(self, student_id, password):
    base_url = "https://horizon.mcgill.ca/pban1/"

    # start the browser
    br = mechanize.Browser()
    br.open(base_url + "twbkwbis.P_WWWLogin")
    br.select_form(name='loginform')

    br.form['sid'] = student_id
    br.form['PIN'] = password

    response = br.submit()
    if 'Authorization Failure' in response.read():
      raise error ("Invalid McGill ID or pin.")

    br.open(base_url + "bzsktran.P_Display_Form?user_type=S&tran_type=V")

    return br.response().read()

  def get_grades_from_html(self, html):
    return re.findall('fieldmediumtext>([^<]*)</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>[1-5]</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault">&nbsp;</TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>([A-Z][+-]?)</SPAN>', html)

  def get_courses_without_grades(self, html):
    return re.findall('fieldmediumtext>([^<]*)</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>[1-5]</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault">&nbsp;</TD>\s*<TD NOWRAP CLASS="dedefault">&nbsp;</TD>', html)

  def write_courses(self, courses):
    with open(".courses", "w") as file:
      for course in courses:
        file.write(course + "|me\n")

  def write_grades(self, grades, file_name="current_grades.txt"):
    with open (file_name, "w") as file:
      output = ""
      for value in grades:
        output = output + value[0] + ":" + value[1] + "|"

      file.write(output)

  def compare_grades(self):
    with open("current_grades.txt", "r") as new:
      contents_new = new.read().split("|")[:-1]
    with open("old_grades.txt", "r") as old:
      contents_old = old.read().split("|")[:-1]

    diff = list(set(contents_new) - set(contents_old))

    return diff

  def notify_recipients(self, diff):
    with open(".friends", "r") as fp:
      friends = dict(s.strip().split(":") for s in fp.readlines())
    with open(".courses", "r") as fp:
      courses = dict([(c, f.split(',')) for c, f in [s.strip().split("|") for s in fp.readlines()]])

    for course in diff:
      course, grade = course.split(":")
      if course in courses:
        self.mail(course, [friends[f] for f in courses[course]], grade)

  def mail(self, course, friends, grade):
    from gmailer import gmailer

    message = "\n".join([
        "Hey,",
        "",
        "I'm here to report that a new grade was posted on Minerva " +
        'for the course "' + course + '". ' +
        "Go check it out if you're interested in seeing how you did.",
        "",
        "Cheers,",
        "Minerva Bot",
        "",
        "http://github.com/selesse/gradechecker"
      ])

    print message

    gmail = gmailer(self.smtp_login, self.smtp_password, "Minerva Bot")
    gmail.send_mail(friends, "[Minerva Grade Checker] " + course, message)

if __name__ == "__main__":
  # check grades
  checker = grade_checker()
  checker.get_grades()
  new_grades = checker.compare_grades()
  if new_grades:
    checker.notify_recipients(new_grades)
    shutil.copyfile("current_grades.txt", "old_grades.txt")
  else:
    print "no new grades were found"
