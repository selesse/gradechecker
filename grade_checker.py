import mechanize, random, re, time, shutil

class grade_checker:
  @staticmethod
  def first_run():
    """First run to generate current_grades."""
    checker = grade_checker()
    (log_file, student_id, password) = checker.load_settings()
    html = checker.get_html(student_id, password)
    grades = checker.get_grades_from_html(html)
    checker.write_grades(grades)
    checker.write_grades(grades, "old_grades.txt")

  def get_grades(self):
    (log, stud_id, password) = checker.load_settings()
    html = checker.get_html(stud_id, password)
    grades = checker.get_grades_from_html(html)
    checker.write_grades(grades)

  def load_settings(self):
    with open(".settings", "r") as settings:
      lines = [x.rstrip() for x in settings.readlines()]
      self.log_file = lines[0]
      self.student_id = lines[1]
      self.password = lines[2]
      self.smtp_login = lines[3]
      self.smtp_password = lines[4]

    return (self.log_file, self.student_id, self.password)

  def get_html(self, student_id, password):
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
    return html

  def get_grades_from_html(self, html):
      return re.findall('fieldmediumtext>([^<]*)</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>[1-5]</SPAN></TD>\s*<TD NOWRAP CLASS="dedefault">&nbsp;</TD>\s*<TD NOWRAP CLASS="dedefault"><SPAN class=fieldmediumtext>([A-Z][+-]?)</SPAN>', html)

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

    if diff:
      self.prep_mail(diff)
      shutil.copyfile("current_grades.txt", "old_grades.txt")


  def prep_mail(self, diff):
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
        "http://github.com/selesse/gradechecker"
      ])

    print message

    gmail = gmailer(self.smtp_login, self.smtp_password, "Minerva Bot")
    gmail.send_mail(friends, "[Minerva Grade Checker] " + course, message)

if __name__ == "__main__":
  # check grades
  checker = grade_checker()
  checker.get_grades()
  checker.compare_grades()
