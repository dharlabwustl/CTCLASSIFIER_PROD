#!/bin/bash
cd /software1/
rm -r /software1/*
git_link=${5}
git clone ${git_link} #https://github.com/dharlabwustl/EDEMA_MARKERS_PROD.git
y=${git_link%.git}
git_dir=$(basename $y)
mv ${git_dir}/* /software1/
chmod +x /software1/*.sh
#$SESSION_ID $XNAT_USER $XNAT_PASS $XNAT_HOST ${git_link} ${program_type}

SESSION_ID=${1}
XNAT_USER=${2}
XNAT_PASS=${3}
XNAT_HOST=${4}
TYPE_OF_PROGRAM=${6}

echo downloadcodefromgithub.sh $*
echo SESSION_ID $SESSION_ID
echo XNAT_USER $XNAT_USER
echo XNAT_PASS $XNAT_PASS
echo XNAT_HOST $XNAT_HOST
echo TYPE_OF_PROGRAM $TYPE_OF_PROGRAM
echo ""



echo /software1/script_to_call_main_program.sh $SESSION_ID $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${TYPE_OF_PROGRAM}
/software1/script_to_call_main_program.sh $SESSION_ID $XNAT_USER $XNAT_PASS ${XNAT_HOST} ${TYPE_OF_PROGRAM}
