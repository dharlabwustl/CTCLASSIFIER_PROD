# docker build -t sharmaatul11/yashengcsfinfarctseg1 .
# docker push  sharmaatul11/yashengcsfinfarctseg1 
# docker run -v $PWD/workinginput:/workinginput -v $PWD/workingoutput:/workingoutput -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v$PWD/output:/output  -it sharmaatul11/yashengcsfinfarctseg1  /Stroke_CT_Processing/call_preproc_segm_session_level_1.sh SNIPR_E03523 
# docker build -t sharmaatul11/dicom2nifti_nwu_1 .
dockerimagename=hosseinclassifier1_prod
./builddockerimage.sh  ${dockerimagename}
 directorytocreate=(output ZIPFILEDIR NIFTIFILEDIR DICOMFILEDIR working input )
#mkdir working
#mkdir input
#mkdir ZIPFILEDIR
#mkdir output
#mkdir NIFTIFILEDIR
#mkdir DICOMFILEDIR
#mkdir software1
#rm -r software1/*
#rm -r DICOMFILEDIR/*
#rm -r NIFTIFILEDIR/*
#rm -r output/*
#rm -r ZIPFILEDIR/*
#rm -r input/*
#rm -r working/*
#
##sessionID=SNIPR_E03523 #SNIPR_E03516
#sessionID=SNIPR_E03614
##docker run -v $PWD/software1:/software1  -v $PWD/NIFTIFILEDIR:/NIFTIFILEDIR  -v $PWD/DICOMFILEDIR:/DICOMFILEDIR  -v $PWD/working:/working -v $PWD/input:/input -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v $PWD/output:/output  -it docker/nrg-repo/sharmaatul11/${dockerimagename}    /callfromgithub/downloadcodefromgithub.sh ${sessionID} $XNAT_USER $XNAT_PASS https://snipr.wustl.edu