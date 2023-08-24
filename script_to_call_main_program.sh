#!/bin/bash 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
export XNAT_HOST=${4}
TYPE_OF_PROGRAM=${5}
echo ${TYPE_OF_PROGRAM}::TYPE_OF_PROGRAM
if [[ ${TYPE_OF_PROGRAM} == 1 ]] ;
then
/software1/call_Classifier_sessionlevel.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS ${4}
fi
if [[ ${TYPE_OF_PROGRAM} == 2 ]] ;
then
/software1/call_Classifier_sessionlevel_SAH.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS ${4}
fi

