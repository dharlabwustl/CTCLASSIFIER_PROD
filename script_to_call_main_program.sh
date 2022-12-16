#!/bin/bash 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
TYPE_OF_PROGRAM=${4}
/software1/call_Classifier_sessionlevel.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS https://snipr.wustl.edu
