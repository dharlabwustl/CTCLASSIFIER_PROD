If you have access to [SNIPR](https://snipr.wustl.edu/), you may use this repository to label the CT scans in a session if they are axial image or not.
Inside the SNIPR you would need to select a session and run the command 
## ct_scan_classifier_usinggithub.

Following is an example how this step can be run in a local computer.
# 1) Set the Docker image name
dockerimagename=hosseinclassifier1_prod


# 2) (Optional) List of dirs you plan to use (not referenced below, kept for clarity)
directorytocreate=(output ZIPFILEDIR NIFTIFILEDIR DICOMFILEDIR working input )

# 3) Create host directories that will be bind-mounted into the container
mkdir working
mkdir input
mkdir ZIPFILEDIR
mkdir output
mkdir NIFTIFILEDIR
mkdir DICOMFILEDIR
mkdir software1

# 4) Clean previous run artifacts (CAUTION: removes contents of these folders)
rm -r software1/*
rm -r DICOMFILEDIR/*
rm -r NIFTIFILEDIR/*
rm -r output/*
rm -r ZIPFILEDIR/*
rm -r input/*
rm -r working/*

# 5) Pick the XNAT session to process
sessionID=SNIPR_E03614

# 6) Run the container:
#    - Bind-mount host folders to container paths
#    - Call in-container script with: sessionID, XNAT creds, and base URL
docker run -v $PWD/software1:/software1  -v $PWD/NIFTIFILEDIR:/NIFTIFILEDIR  -v $PWD/DICOMFILEDIR:/DICOMFILEDIR  -v $PWD/working:/working -v $PWD/input:/input -v $PWD/ZIPFILEDIR:/ZIPFILEDIR -v $PWD/output:/output  -it docker/nrg-repo/sharmaatul11/${dockerimagename}    /callfromgithub/downloadcodefromgithub.sh ${sessionID} $XNAT_USER $XNAT_PASS https://snipr.wustl.edu
