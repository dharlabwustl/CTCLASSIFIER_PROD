#!/usr/bin/env bash
parent_dir=${1}
echo 'FROM hossein15051/stroke_edema:scan_selection_v1_20201005' > ${parent_dir}/Dockerfile
echo 'RUN sed -i -e s/deb.debian.org/archive.debian.org/g \' >> ${parent_dir}/Dockerfile
echo            '-e s|security.debian.org|archive.debian.org/|g \' >> ${parent_dir}/Dockerfile
echo         '-e /stretch-updates/d /etc/apt/sources.list' >> ${parent_dir}/Dockerfile
#directory_of_software="/donotuse"
#echo 'RUN apt update' >> ${parent_dir}/Dockerfile
#echo 'RUN mv /run /donotuse' >> ${parent_dir}/Dockerfile
#echo 'RUN rm  /donotuse/Classifier_wholeSession.py' >> ${parent_dir}/Dockerfile
#echo 'RUN rm  /donotuse/label_probability.py' >> ${parent_dir}/Dockerfile
echo 'RUN mkdir -p /callfromgithub' >> ${parent_dir}/Dockerfile
echo 'RUN chmod 755 /callfromgithub' >> ${parent_dir}/Dockerfile
echo 'COPY downloadcodefromgithub.sh /callfromgithub/' >> ${parent_dir}/Dockerfile
echo 'RUN chmod +x /callfromgithub/downloadcodefromgithub.sh' >> ${parent_dir}/Dockerfile
echo 'RUN apt -y update'
#echo 'WORKDIR /donotuse' >> ${parent_dir}/Dockerfile
ubuntupackagestoinstall=(vim zip unzip curl tree)
echo ${ubuntupackagestoinstall[0]}
len_array=${#ubuntupackagestoinstall[@]}
last_num=$((len_array -1))
echo $last_num
echo "RUN apt install -y \\" >> ${parent_dir}/Dockerfile 
for x in ${ubuntupackagestoinstall[@]} ; do 
	if [[ $x = ${ubuntupackagestoinstall[last_num]} ]] ; then
		echo "  ${x}  " >> ${parent_dir}/Dockerfile
	else 
		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
fi 
done

pipinstall=(PyGithub pandas)
len_array=${#pipinstall[@]}
last_num=$((pipinstall -1))
echo "RUN pip install \\" >> ${parent_dir}/Dockerfile
for x in ${pipinstall[@]} ; do
	if [[ $x = ${pipinstall[last_num]} ]] ; then
		echo "  ${x}  " >> ${parent_dir}/Dockerfile
	else
		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
fi
done


#echo "COPY  \\" >> ${parent_dir}/Dockerfile
#for x in *.sh; do
#
#		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
#
#done
#echo "/${directory_of_software}/  " >> ${parent_dir}/Dockerfile
#echo "COPY  \\" >> ${parent_dir}/Dockerfile
#for x in *.py ; do
#
#		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
#
#done
#echo "/${directory_of_software}/  " >> ${parent_dir}/Dockerfile
#echo "RUN  \\" >> ${parent_dir}/Dockerfile
## for x in ${changemodes_sh[@]} ; do


counter=0
#
#total_num_sh_files=$(ls -l *.sh | grep ^- | wc -l)
#total_num_sh_files=$((total_num_sh_files-1))
#for x in *.sh ; do
#	# if [[ $x = ${changemodes_sh[last_num]} ]] ; then
#		if [[ $counter -eq ${total_num_sh_files} ]] ; then
#		echo " chmod +x  /${directory_of_software}/${x}  " >> ${parent_dir}/Dockerfile
#	else
#		echo " chmod +x /${directory_of_software}/${x}  &\\ " >> ${parent_dir}/Dockerfile
#fi
#counter=$((counter+1))
#done

# pipinstall=(nibabel numpy xmltodict pandas requests pydicom python-gdcm glob2 scipy pypng )
# len_array=${#pipinstall[@]}
# last_num=$((pipinstall -1))
# echo "RUN pip install \\" >> ${parent_dir}/Dockerfile 
# for x in ${pipinstall[@]} ; do 
# 	if [[ $x = ${pipinstall[last_num]} ]] ; then
# 		echo "  ${x}  " >> ${parent_dir}/Dockerfile
# 	else 
# 		echo "  ${x}  \\ " >> ${parent_dir}/Dockerfile
# fi 
# done


# copyfiles_sh=(call_Classifier_scanlevel) # dicom2nifti_call_subjectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_alllevels_selected dicom2nifti_call_projectlevel_selected  dicom2nifti_call_sessionlevel_selected dicom2nifti_call_scanlevel_selected  dicom2nifti_call_scanlevel writetowebpagetable_call label_session_call call_downloadwithrequest )
# len_array=${#copyfiles_sh[@]}
# last_num=$((copyfiles_sh -1))
# echo "COPY  \\" >> ${parent_dir}/Dockerfile 
# for x in ${copyfiles_sh[@]} ; do 
 
# 		echo "  ${x}.sh  \\ " >> ${parent_dir}/Dockerfile

# done
# echo "/donotuse/  " >> ${parent_dir}/Dockerfile 

# copyfiles_py=(Classifier_wholeSession label_probability) #dicom2nifiti_projectlevel_selected dicom2nifiti_subjectlevel_selected dicom2nifiti_subjectlevel_selected  dicom2nifiti_alllevels_selected dicom2nifiti_projectlevel_selected dicom2nifiti_sessionlevel_selected dicom2nifiti_scanlevel_selected DecompressDCM dicom2nifiti_sessionlevel xnatSession dicom2nifiti_scanlevel writetowebpagetable label_session_Atul downloadwithrequest label_probability)
# len_array=${#copyfiles_py[@]}
# last_num=$((copyfiles_py -1))
# echo "COPY  \\" >> ${parent_dir}/Dockerfile 
# for x in ${copyfiles_py[@]} ; do 
 
# 		echo "  ${x}.py  \\ " >> ${parent_dir}/Dockerfile

# done
# echo "/donotuse/  " >> ${parent_dir}/Dockerfile 
# echo "COPY stroke_edema_template.xml /donotuse/" >> ${parent_dir}/Dockerfile

# changemodes_sh=(call_Classifier_scanlevel) #dicom2nifti_call_projectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_alllevels_selected dicom2nifti_call_projectlevel_selected dicom2nifti_call_sessionlevel_selected dicom2nifti_call_scanlevel_selected dicom2nifti_call_scanlevel writetowebpagetable_call  label_session_call  call_downloadwithrequest )

# len_array=${#changemodes_sh[@]}
# last_num=$((changemodes_sh -1))
# echo "RUN  \\" >> ${parent_dir}/Dockerfile 
# for x in ${changemodes_sh[@]} ; do 
# 	if [[ $x = ${changemodes_sh[last_num]} ]] ; then
# 		echo " chmod +x  /donotuse/${x}.sh  " >> ${parent_dir}/Dockerfile
# 	else 
# 		echo " chmod +x /donotuse/${x}.sh  &\\ " >> ${parent_dir}/Dockerfile
# fi 
# done

