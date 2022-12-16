#!/usr/bin/env bash
echo 'FROM hossein15051/stroke_edema:scan_selection_v1_20201005' > Dockerfile

#directory_of_software="/donotuse"
#echo 'RUN apt update' >> Dockerfile
#echo 'RUN mv /run /donotuse' >> Dockerfile
#echo 'RUN rm  /donotuse/Classifier_wholeSession.py' >> Dockerfile
#echo 'RUN rm  /donotuse/label_probability.py' >> Dockerfile
echo 'RUN mkdir -p /callfromgithub' >> Dockerfile
echo 'RUN chmod 755 /callfromgithub' >> Dockerfile
echo 'COPY downloadcodefromgithub.sh /callfromgithub/' >> Dockerfile
echo 'RUN chmod +x /callfromgithub/downloadcodefromgithub.sh' >> Dockerfile

#echo 'WORKDIR /donotuse' >> Dockerfile
ubuntupackagestoinstall=(vim zip unzip curl tree)
echo ${ubuntupackagestoinstall[0]}
len_array=${#ubuntupackagestoinstall[@]}
last_num=$((len_array -1))
echo $last_num
echo "RUN apt install -y \\" >> Dockerfile 
for x in ${ubuntupackagestoinstall[@]} ; do 
	if [[ $x = ${ubuntupackagestoinstall[last_num]} ]] ; then
		echo "  ${x}  " >> Dockerfile
	else 
		echo "  ${x}  \\ " >> Dockerfile
fi 
done

pipinstall=(PyGithub)
len_array=${#pipinstall[@]}
last_num=$((pipinstall -1))
echo "RUN pip install \\" >> Dockerfile
for x in ${pipinstall[@]} ; do
	if [[ $x = ${pipinstall[last_num]} ]] ; then
		echo "  ${x}  " >> Dockerfile
	else
		echo "  ${x}  \\ " >> Dockerfile
fi
done


#echo "COPY  \\" >> Dockerfile
#for x in *.sh; do
#
#		echo "  ${x}  \\ " >> Dockerfile
#
#done
#echo "/${directory_of_software}/  " >> Dockerfile
#echo "COPY  \\" >> Dockerfile
#for x in *.py ; do
#
#		echo "  ${x}  \\ " >> Dockerfile
#
#done
#echo "/${directory_of_software}/  " >> Dockerfile
#echo "RUN  \\" >> Dockerfile
## for x in ${changemodes_sh[@]} ; do


counter=0
#
#total_num_sh_files=$(ls -l *.sh | grep ^- | wc -l)
#total_num_sh_files=$((total_num_sh_files-1))
#for x in *.sh ; do
#	# if [[ $x = ${changemodes_sh[last_num]} ]] ; then
#		if [[ $counter -eq ${total_num_sh_files} ]] ; then
#		echo " chmod +x  /${directory_of_software}/${x}  " >> Dockerfile
#	else
#		echo " chmod +x /${directory_of_software}/${x}  &\\ " >> Dockerfile
#fi
#counter=$((counter+1))
#done

# pipinstall=(nibabel numpy xmltodict pandas requests pydicom python-gdcm glob2 scipy pypng )
# len_array=${#pipinstall[@]}
# last_num=$((pipinstall -1))
# echo "RUN pip install \\" >> Dockerfile 
# for x in ${pipinstall[@]} ; do 
# 	if [[ $x = ${pipinstall[last_num]} ]] ; then
# 		echo "  ${x}  " >> Dockerfile
# 	else 
# 		echo "  ${x}  \\ " >> Dockerfile
# fi 
# done


# copyfiles_sh=(call_Classifier_scanlevel) # dicom2nifti_call_subjectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_alllevels_selected dicom2nifti_call_projectlevel_selected  dicom2nifti_call_sessionlevel_selected dicom2nifti_call_scanlevel_selected  dicom2nifti_call_scanlevel writetowebpagetable_call label_session_call call_downloadwithrequest )
# len_array=${#copyfiles_sh[@]}
# last_num=$((copyfiles_sh -1))
# echo "COPY  \\" >> Dockerfile 
# for x in ${copyfiles_sh[@]} ; do 
 
# 		echo "  ${x}.sh  \\ " >> Dockerfile

# done
# echo "/donotuse/  " >> Dockerfile 

# copyfiles_py=(Classifier_wholeSession label_probability) #dicom2nifiti_projectlevel_selected dicom2nifiti_subjectlevel_selected dicom2nifiti_subjectlevel_selected  dicom2nifiti_alllevels_selected dicom2nifiti_projectlevel_selected dicom2nifiti_sessionlevel_selected dicom2nifiti_scanlevel_selected DecompressDCM dicom2nifiti_sessionlevel xnatSession dicom2nifiti_scanlevel writetowebpagetable label_session_Atul downloadwithrequest label_probability)
# len_array=${#copyfiles_py[@]}
# last_num=$((copyfiles_py -1))
# echo "COPY  \\" >> Dockerfile 
# for x in ${copyfiles_py[@]} ; do 
 
# 		echo "  ${x}.py  \\ " >> Dockerfile

# done
# echo "/donotuse/  " >> Dockerfile 
# echo "COPY stroke_edema_template.xml /donotuse/" >> Dockerfile

# changemodes_sh=(call_Classifier_scanlevel) #dicom2nifti_call_projectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_subjectlevel_selected dicom2nifti_call_alllevels_selected dicom2nifti_call_projectlevel_selected dicom2nifti_call_sessionlevel_selected dicom2nifti_call_scanlevel_selected dicom2nifti_call_scanlevel writetowebpagetable_call  label_session_call  call_downloadwithrequest )

# len_array=${#changemodes_sh[@]}
# last_num=$((changemodes_sh -1))
# echo "RUN  \\" >> Dockerfile 
# for x in ${changemodes_sh[@]} ; do 
# 	if [[ $x = ${changemodes_sh[last_num]} ]] ; then
# 		echo " chmod +x  /donotuse/${x}.sh  " >> Dockerfile
# 	else 
# 		echo " chmod +x /donotuse/${x}.sh  &\\ " >> Dockerfile
# fi 
# done

