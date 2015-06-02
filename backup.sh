#!/bin/bash
DATE=$(date +%F)
TARFILE=db-$DATE.tar.gz
tar -cvpzf /home/odin/app-backups/$TARFILE /var/www/incentives-app/app.db
