#!/usr/bin/env bash
# mkdir /input
# mkdir /working
export XNAT_USER=${2}
export XNAT_PASS=${3}
export XNAT_HOST=${4} #"https://snipr-dev-test1.nrg.wustl.edu"
sessionId=$1          #SNIPR_E03539 #SNIPR_E03526
function wait_for_file() {
  local file_to_wait=${1} #${filename}
  local sleep_second=1
  local sleep_second_counter=0
  while [ ! -e ${file_to_wait} ]; do
    sleep ${sleep_second}
    sleep_second_counter=$((sleep_second_counter + 1))
    if [ ${sleep_second_counter} -gt 10 ]; then
      echo sleep_second_counter::${sleep_second_counter} >>/output/error.txt
      break
    fi
    echo sleep_second_counter::${sleep_second_counter} >>/output/error.txt
  done

}
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
output_directory=/output/
filename=${output_directory}/${sessionId}.csv
call_get_metadata_session_saveascsv_arguments=('call_get_metadata_session_saveascsv' ${sessionId} ${filename})
outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_get_metadata_session_saveascsv_arguments[@]}")
wait_for_file ${filename}
echo outputfiles_present::${outputfiles_present} >>/output/error.txt
while IFS=',' read -ra array; do
  URI=${array[6]}
  echo "URI":${URI}
  resource_dir="DICOM"
  output_csvfile=${sessionId}_${array[4]}.csv
  echo "output_csvfile":${output_csvfile}
  dir_to_receive_the_data=${output_directory}
  call_get_resourcefiles_metadata_saveascsv_args_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile} )
  outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_get_resourcefiles_metadata_saveascsv_args_arguments[@]}")
  wait_for_file ${dir_to_receive_the_data}/${output_csvfile}
done < <(tail -n +2 "${filename}")
