#!/bin/bash

echo $1
mysqldump --user=foneloan --host=192.168.82.66 --password="$1" fone_credit_f1 | gzip > /home/foneloan/core/migrate_db/Backup/fone_credit_f1'_'$(date +'%Y-%m-%d').sql.gz