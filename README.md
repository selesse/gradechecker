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
