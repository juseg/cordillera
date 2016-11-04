#!/bin/bash

filename=cordillera-cycle.tex
errcount=0

echo "Looping back through all commits."
echo "date,words" | tee count.csv

for c in $(git rev-list master); do
	git checkout -q $c
  date=$(git log -1  --date=iso --pretty=format:%ad $commit)
  words=$(texcount -template="{SUM}" ../$filename)
	if [[ $words =~ ^[0-9]+$ ]]
  then
    echo "$date,$words" | tee -a count.csv
  else
    echo "$date,ERROR"
    errcount=$((errcount+1))
  fi
done

echo "Done, $errcount erroneous commits ignored."

git checkout master
