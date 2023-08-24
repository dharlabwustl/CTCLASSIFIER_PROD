#!/usr/bin/env bash
parent_dir=${1}
#${parent_dir}/bashtowriteDockerfile.sh  ${parent_dir}
command=""
for x in ${parent_dir}/*.json ;
do 
	command="${command}   ${x}  "
done
echo $command
python /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/FROM_DOCUMENTS/docker-images/command2label.py  $command  >> ${parent_dir}/Dockerfile
 imagename=$2
 repository_name=${3}
#imagename=hosseinclassifier1
#docker login registry.nrg.wustl.edu
#docker build -t docker/nrg-repo/sharmaatul11/${imagename} .
#docker login registry.nrg.wustl.edu
#docker push docker/nrg-repo/sharmaatul11/${imagename}
# docker run -v $PWD:/mounted_directory -it   sharmaatul11/${imagename}  /bin/bash
#docker build -t registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename} ${parent_dir}
#docker push registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename}
cd ${parent_dir}
docker build -t ${repository_name}/${imagename} ${parent_dir}
docker push ${repository_name}/${imagename}