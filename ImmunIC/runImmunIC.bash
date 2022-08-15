#!/bin/bash
# Bash script to run ImmunIC
# Usage: bash runImmunIC.bash input_csv_file

inputfile=$1

if [ ! -f $inputfile ]; then
   echo $inputfile "not found"
   exit
fi

immunic_path=`dirname "$(realpath $0)"`
python3 $immunic_path/xgboost-cd4cd8Tcells.py $inputfile
python3 $immunic_path/ImmunIC.py $inputfile
