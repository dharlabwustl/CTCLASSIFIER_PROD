#!/bin/bash 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST=${4}
TYPE_OF_PROGRAM=${5}
echo ${TYPE_OF_PROGRAM}::TYPE_OF_PROGRAM
if [[ ${TYPE_OF_PROGRAM} == 1 ]] ;
then
/software1/call_Classifier_sessionlevel.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS https://snipr.wustl.edu
fi

