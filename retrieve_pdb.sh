#!/bin/bash

printf "release\tpdb\n" > pdb.stat

curl https://www.rcsb.org/pdb/results/contentGrowthCsv.do?format=total|grep -P '\d+\",\"[.\d]+\",\"[.\d]+'|sed "s/,/\t/g"|sed 's/"//g'|cut -f1,3|sort -k1n |grep -v -P "\s0.0$">> pdb.stat
