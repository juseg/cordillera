#!/bin/bash

f=cordillera-climate.tex

cd ..

printf "date,words\n"
for c in $(git rev-list master); do
	git checkout -q $c
	printf "$(git log -1  --date=iso --pretty=format:%ad $commit),"
	printf "$(texcount -merge -nosub -template="{SUM}" $f)\n"
done

git checkout master
