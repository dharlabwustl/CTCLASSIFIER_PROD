#!/usr/bin/env bash
 ./bashtowriteDockerfile.sh
command=""
for x in *.json ;
do 
	command="${command}   ${x}  "
done
echo $command
python /media/atul/WDJan2022/WASHU_WORKS/PROJECTS/FROM_DOCUMENTS/docker-images/command2label.py  $command  >> ./Dockerfile
 imagename=$1
#imagename=hosseinclassifier1
docker login registry.nrg.wustl.edu
#docker build -t docker/nrg-repo/sharmaatul11/${imagename} .
#docker login registry.nrg.wustl.edu
#docker push docker/nrg-repo/sharmaatul11/${imagename}
# docker run -v $PWD:/mounted_directory -it   sharmaatul11/${imagename}  /bin/bash
docker build -t registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename} .
docker push registry.nrg.wustl.edu/docker/nrg-repo/sharmaatul11/${imagename}
