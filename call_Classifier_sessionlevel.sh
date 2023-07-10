#!/usr/bin/env bash
# mkdir /input 
# mkdir /working
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
sessionId=$1 #SNIPR_E03539 #SNIPR_E03526

#file_to_wait=$1
#while [ ! –e ${file_to_wait} ]
#do
#  sleep 1
#done
#
#echo “${file_to_wait} has been created”
# scanID=$2 #8
# rm -r /ZIPFILEDIR/*
# cp /mounted_directory/Classifier_wholeSession.py /run/Classifier_wholeSession.py 
# cd /run/
# echo $PWD
#python /software1/Classifier_session_level.py /input /working ${sessionId}  #${scanID}

call_classifier_v1_arguments=('call_classifier_v1' /input /working ${sessionId})
outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py  "${call_classifier_v1_arguments[@]}")
