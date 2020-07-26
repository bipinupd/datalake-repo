#!/bin/bash
enterprise=$1
work=$2
landing=$3
for sql_file in `find /workspace/schemas -name *.ddl`
do
  cat "$sql_file" | sed -e "s/_ENTERPRISE/$1/g; s/_WORK/$2/g; s/_LANDING/$3/g" | bq query --use_legacy_sql=false  
done
