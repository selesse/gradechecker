gradechecker
============

The McGill Minerva grade checker. It will go check to see if you have new
grades up on Minerva and email you and a list of subscribers if it finds
some.

Requirements
------------
* bash
* python
* mechanize (http://pypi.python.org/packages/source/m/mechanize/mechanize-0.2.5.tar.gz)

Setup
-----
cd into the directory

    ./configure.sh

Answer the questions, then whenever you feel like checking for grades...

    python grade_checker.py

Adding subscribers
------------------
To add subscribers to your notifications, open the .friends file. For every
new subscriber, add an entry for them of the form "alias:email".

Then, for every course you want to subscribe them to, open the .courses file.
Add them to every course you want (comma delimited, no spaces needed).
