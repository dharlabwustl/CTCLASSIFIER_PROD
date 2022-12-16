#!/usr/bin/env bash
# mkdir /input 
# mkdir /working
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
sessionId=$1 #SNIPR_E03539 #SNIPR_E03526
# scanID=$2 #8
# rm -r /ZIPFILEDIR/*
# cp /mounted_directory/Classifier_wholeSession.py /run/Classifier_wholeSession.py 
# cd /run/
# echo $PWD
python /software1/Classifier_session_level.py /input /working ${sessionId}  #${scanID} 