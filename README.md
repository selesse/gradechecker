gradechecker
============

minerva gradechecker

Requirements
------------
* mechanize (http://pypi.python.org/packages/source/m/mechanize/mechanize-0.2.5.tar.gz)

Setup
-----
* Create a .settings file that follows this structure:

    path/to/logfile
    mcgill username
    mcgill password
    gmail_username
    gmail_password

The gmail username and gmail password are for the email notifier.

* Create a .friends file that follows this structure:

    name:email
    name2:email2

* Create a .courses file that follows this structure:

    course name|comma-separated list of students
    Intro to Software|me,steve

Where "course name" is what appears on the unofficial transcript page.
