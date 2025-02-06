#!/bin/bash 

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
export XNAT_HOST=${4}
TYPE_OF_PROGRAM=${5}
echo ${TYPE_OF_PROGRAM}::TYPE_OF_PROGRAM

echo script_to_call_main_program.sh $*
echo SESSION_ID $SESSION_ID
echo XNAT_USER  $XNAT_USER
echo XNAT_PASS  $XNAT_PASS
echo XNAT_HOST  $XNAT_HOST
echo TYPE_OF_PROGRAM $TYPE_OF_PROGRAM
echo ""

if [[ ${TYPE_OF_PROGRAM} == 1 ]] ;
then
echo /software1/call_Classifier_sessionlevel.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS ${4}
/software1/call_Classifier_sessionlevel.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS ${4}
fi
if [[ ${TYPE_OF_PROGRAM} == 2 ]] ;
then
/software1/call_Classifier_sessionlevel_SAH.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS ${4}
fi

#########################
if [[ ${TYPE_OF_PROGRAM} == 'PROJECT_LEVEL_SCAN_CLASSIFIER' ]] ;
then
/software1/project_level_classifier.sh ${SESSION_ID} $XNAT_USER $XNAT_PASS ${4}
fi

