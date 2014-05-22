#!/bin/bash

f=cordillera-cycle.tex

printf "date,words\n" > count.csv
for c in $(git rev-list master); do
	git checkout -q $c
	printf "$(git log -1  --date=iso --pretty=format:%ad $commit),"
	printf "$(texcount -template="{SUM}" ../$f)\n"
done >> count.csv

git checkout master
