#!/bin/bash

var=a
if echo "$var" | egrep -q '^\-?[0-9]*\.?[0-9]+$'; then    

        echo "$var is a number"

else    

        echo "$var is not a number"

fi
