#!/bin/bash

set -e

function run_python_first_run() {
  python -c \
  "from grade_checker import grade_checker; grade_checker.first_run()" \
  > /dev/null
}

settings=".settings"

echo "Welcome to the McGill Minerva grade checker."
echo ""
read -p  "Log file name [grade-checker.txt]: " log_file
read -p  "Email to send notifications to: " email
read -p  "Notifier email (gmail only): " gmail_email
read -sp "Notifier email password:" gmail_pass
read -p  "McGill student id: " student_id
read -sp "Password: " password

if [ -z "$log_file" ] ; then
  log_file="grade-checker.txt"
fi

if [ -e "$settings" ] ; then
  echo "Settings file already exists, try clearing $settings."
else
  echo -e "$log_file\n$student_id\n$password\n$gmail_email\n$gmail_pass" \
    > $settings
  echo -e "me:$email" > .friends
  echo -e "\n\nGetting initial copy of grades..."
  run_python_first_run
  echo "Done."
fi
