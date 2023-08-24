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
scanID=$2 #8
rm -r /ZIPFILEDIR/*
# cp /mounted_directory/Classifier_wholeSession.py /run/Classifier_wholeSession.py
cd /run/
echo $PWD
#python /software1/Classifier_session_level_SAH.py /input /working ${sessionId}  #${scanID}

#output_directory=/output/
#filename=${output_directory}/${sessionId}.csv
#call_get_metadata_session_saveascsv_arguments=('call_get_metadata_session_saveascsv' ${sessionId} ${filename})
#outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_get_metadata_session_saveascsv_arguments[@]}")
#wait_for_file ${filename}
#echo outputfiles_present::${outputfiles_present} >>/output/error.txt
##while IFS=',' read -ra array; do
#  ################################################
#  sessionDir=/DICOMFILEDIR
#  workingDir=/input      # args.stuff[2]
#  sessionId=${sessionId} # args.stuff[3]
#  call_classifier_v1_arguments=('call_classifier_v1' ${sessionId} ${workingDir} ${sessionId})
#  outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_classifier_v1_arguments[@]}")
#  echo outputfiles_present::${outputfiles_present}
#  ################################################
#  #
#  #  URI=${array[6]}
#  #  #  echo "URI":${URI}
#  #  resource_dir="DICOM"
#  #  output_csvfile=${sessionId}_SCANSCANTEMP_${array[4]}.csv
#  #  #  echo "output_csvfile":${output_csvfile}
#  #  dir_to_receive_the_data=${output_directory}
#  #  call_get_resourcefiles_metadata_saveascsv_args_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile})
#  #  outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_get_resourcefiles_metadata_saveascsv_args_arguments[@]}")
#  #  wait_for_file ${dir_to_receive_the_data}/${output_csvfile}
#  #  SCAN_ID=${array[4]}
#  #
#  #  if [ ${SCAN_ID} == "2" ]; then
#  #    call_sort_dicom_list_arguments=('call_sort_dicom_list' ${dir_to_receive_the_data}/${output_csvfile})
#  #    outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_sort_dicom_list_arguments[@]}")
#  #    echo "SCAN_ID::${SCAN_ID}"
#  #    while IFS=',' read -ra array1; do
#  #      url=${array1[6]}
#  #      #    echo url::${url}
#  #      dicom_filename=${array1[8]}
#  #      #    echo dicom_filename::${dicom_filename}
#  #      #    filename=args.stuff[2]
#  #
#  #      dir_to_save=/DICOMFILEDIR ##args.stuff[3]
#  #      call_download_a_singlefile_with_URIString_arguments=('call_download_a_singlefile_with_URIString' ${url} ${dicom_filename} ${dir_to_save})
#  ##      outputfiles_present=$(python /software1/Classifier_session_level_v1_5July2023.py "${call_download_a_singlefile_with_URIString_arguments[@]}")
#  #
#  #
#  #
#  #    done < <(tail -n +2 "${dir_to_receive_the_data}/${output_csvfile}")
#  #
#  #    break
#  #  fi
##done < <(tail -n +2 "${filename}")
