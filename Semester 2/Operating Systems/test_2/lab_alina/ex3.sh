#!/bin/bash

sum=0
count=0
div5=0

read n
while [ $n -ne 0 ]
do
	echo $n
	sum=`expr $sum + $n`
	count=$((count+1))
	if [ `expr $n % 5` -eq 0 ]; then
		div5=$((div5+1))
	fi
	read n
done

echo Ended with zero
echo Sum is $sum, average is $((sum/count)).
echo $div5 numbers are divisible by 5.
