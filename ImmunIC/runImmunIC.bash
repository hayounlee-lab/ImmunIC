#!/bin/bash
# Bash file to run ImmunIC
# Usage: bash runImmunIC.bash input_csv_file

inputfile=$1
if [ ! -f $1 ]; then
   echo $1" not found"
   exit
fi

python3 /root/ImmunIC/xgboost-cd4cd8Tcells.py $inputfile
python3 /root/ImmunIC/ImmunIC.py $inputfile
