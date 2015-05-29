#!/bin/bash
#Install and enable mod_wsgi
apt-get install libapache2-mod-wsgi python-dev 2>> setup-error.log
a2enmod wsgi 2>> setup-error.log

#Setup virtualenv and install all dependencies
apt-get install python-pip 2>> setup-error.log
pip install virtualenv 2>> setup-error.log
virtualenv venv 2>> setup-error.log
source venv/bin/active 2>> setup-error.log
pip install -r requirments.txt 2>> setup-error.log

#Check for db files and backup directory
if [ ! -f app.db ];
then
  touch app.db
  echo "No app database found. Creating..."
fi

if [ ! -f test.bd ] && [ -f tests.py ];
then
  touch test.db
  echo "No test database found. Creating..."
fi

if [ ! -d ../app-backups ];
then
  mkdir ../app-backups
  echo "Made backup directory $(readlink -f ../app-backups)"
fi

#Set cronjob to backup db daily at midnight
crontab -l > mycron
echo "0 0 * * * backup.sh" >> mycron
crontab mycron 2>> setup-error.log
rm mycron
echo "Scheduled backups for once a day at midnight in $(readlink -f ../app-backups)"
