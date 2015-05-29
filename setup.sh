#!/bin/bash

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

crontab -l > mycron
echo "0 0 * * * backup.sh" >> mycron
crontab mycron
rm mycron
echo "Scheduled backups for once a day at midnight in $(readlink -f ../app-backups)"
