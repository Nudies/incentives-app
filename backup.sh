#!/bin/bash
DATE=$(date +%F)
TARFILE=db-$DATE.tar.gz
tar -cvpzf $(readlink -f ../app-backups)/$TARFILE $(readlink -f app.db)