#!/usr/bin/python
import urllib.parse
import os, sys, errno, shutil, uuid
import math,json
import glob
import re
import pandas as pd
import requests
import pydicom as dicom
import subprocess
from xnatSession import XnatSession
import DecompressDCM
import label_probability
from updatemysql import insert_data,update_or_create_column_with_given_session_only
# Prep XNAT session
XNAT_HOST =os.environ['XNAT_HOST'] #'https://snipr.wustl.edu' #'http://snipr02.nrg.wustl.edu:8080' # 'https://snipr.wustl.edu' #os.environ['XNAT_HOST']#
XNAT_USER = os.environ['XNAT_USER']
XNAT_PASS = os.environ['XNAT_PASS']
catalogXmlRegex = re.compile(r'.*\.xml$')
xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
xnatSession.renew_httpsession()
def get_slice_idx(nDicomFiles):
    return min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain
def get_metadata_session(sessionId):
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    #xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    return metadata_session

def get_dicom_from_filesystem(sessionId, scanId,xnatSession):
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
    print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" %
           (sessionId, scanId))
    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    if response.status_code != 200:
        raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId,
                                                                              response.status_code,
                                                                              response.reason,
                                                                              response.text))
    result = response.json()['ResultSet']['Result']
    # print(result[0]) #['absolutePath'])
    nDicomFiles = len(result)
    # print(nDicomFiles)
    if nDicomFiles == 0:
        raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    ###########################################################################
    scanDir='/input'
    # if not os.path.isdir(scanDir):
    #     continue
    for dcm in glob.iglob(os.path.join(scanDir, "**"), recursive=True):
        try:
            # Test if it's a DICOM file
            dicomDs = dicom.filereader.dcmread(dcm)
            # Gather all in series and return the slice 70% thru brain
            dicomFiles = [fl for fl in glob.iglob(os.path.join(os.path.dirname(dcm), "*")) if not catalogXmlRegex.match(fl)]
            nDicomFiles = len(dicomFiles)
            selDicom = dicomFiles[get_slice_idx(nDicomFiles)]
            print("Found %s DICOM files, using %s for snapshot" % (nDicomFiles, selDicom))
            return selDicom, nDicomFiles
        except (dicom.errors.InvalidDicomError, IsADirectoryError):
            # Skip, not a dicom
            pass
    raise Exception("No DICOM files found for %s" % scanId)
def get_resourcefiles_metadata(URI,resource_dir):
    url = (URI+'/resources/' + resource_dir +'/files?format=json')
    print(url)
    #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    #xnatSession.close_httpsession())
    metadata_masks=response.json()['ResultSet']['Result']
    return metadata_masks
def get_dicom_using_xnat(sessionId, scanId,xnatSession):
    # #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)

    scan_URI=f'/data/experiments/{sessionId}/scans/{scanId}'
    dicomfolder_metadata=get_resourcefiles_metadata(scan_URI,'DICOM')
    dicomfolder_metadata_df = pd.read_json(json.dumps(dicomfolder_metadata))
    # url = ("/data/experiments/%s/scans/%s/resources/DICOM/files?format=json&locator=absolutePath&file_format=DICOM" %
    #        (sessionId,scanId ))
    # print(url)
    # #xnatSession.renew_httpsession()
    # response = xnatSession.httpsess.get(xnatSession.host + url)
    #
    # result = response.json()['ResultSet']['Result']
    nDicomFiles =dicomfolder_metadata_df.shape[0] # len(result)
    if nDicomFiles == 0:
        raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    #     # Get 70% file and ensure it exists
    selDicomAbs =dicomfolder_metadata_df.loc[get_slice_idx(nDicomFiles),'URI'] #result[get_slice_idx(nDicomFiles)]['absolutePath']
    print(selDicomAbs)
    #     # selDicomAbs_split=selDicomAbs.split('/')
    #     # print(selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3])
    #     ######################################################################################

    #     # print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/resources/DICOM/files?format=zip" %
           (sessionId, scanId))
    print(url)

    #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename='/ZIPFILEDIR/' + sessionId + scanId + '.zip'
    #############################
    print(zipfilename)
    print('/ZIPFILEDIR')
    subprocess.call("echo '' >> /tmp/log.txt",shell=True)
    subprocess.call("echo Starting new run >> /tmp/log.txt",shell=True)
    subprocess.call("pwd >> /tmp/log.txt",shell=True)
    subprocess.call("ls -la >> /tmp/log.txt",shell=True)
    subprocess.call("whoami >> /tmp/log.txt",shell=True)
    subprocess.call("id -u >> /tmp/log.txt",shell=True)
    subprocess.call('ls -la /ZIPFILEDIR >> /tmp/log.txt',shell=True)
    subprocess.call('echo about to open zip file >> /tmp/log.txt',shell=True)
    ###############################
    with open(zipfilename, "wb") as f:
        print("Zip file opened")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    ############################
    print("Zip file stored")
    subprocess.call("ls -la /ZIPFILEDIR >> /tmp/log.txt",shell=True)
    #####################
    command = 'unzip -d /ZIPFILEDIR ' + zipfilename
    subprocess.call(command,shell=True)
    #########################
    print("Unzip -d complete")
    command = 'find /ZIPFILEDIR -type f >> /tmp/log.txt'
    subprocess.call(command,shell=True)
    ######################

    command = 'cp  /ZIPFILEDIR/*/*/*/*/*/*/*.dcm  /DICOMFILEDIR/ '
    subprocess.call(command,shell=True)
    subprocess.call('ls -la /DICOMFILEDIR >> /tmp/log.txt',shell=True)
    #     #################################################################
    sessionDir='/DICOMFILEDIR'

    selDicomAbs =dicomfolder_metadata_df.loc[get_slice_idx(nDicomFiles),'URI']  # result[get_slice_idx(nDicomFiles)]['absolutePath']
    # #/ZIPFILEDIR/BJH_011_13102019_0715/*/*/*/*/**
    selDicom=os.path.join(sessionDir,os.path.basename(selDicomAbs))
    print(selDicom)
    return selDicom, nDicomFiles


def run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession):
    # def run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSesDir, xnatSession):
    print("Classifying scan %s" % scanId)
    # Select DICOM file for scanId (70% thru the brain)
    selDicom, nDicomFiles = get_dicom_using_xnat(sessionId, scanId,xnatSession) #, sessionDir, xnatSesDir, xnatSession)
    # selDicom, nDicomFiles = get_dicom_from_filesystem(sessionId, scanId,xnatSession)
    print(selDicom)
    print(nDicomFiles)
    ####################################################################
    selDicomDecompr = os.path.join(rawDir, os.path.basename(selDicom))
    DecompressDCM.decompress(selDicom, selDicomDecompr)
    # Classify it
    label = label_probability.classify(selDicomDecompr, jpgDir, scanId, nDicomFiles)
    print("Scan classification for %s scan %s is '%s'" % (sessionId, scanId, label))
    # Change value of series_class in XNAT
    # url = ("/data/experiments/%s/scans/%s?xsiType=xnat:mrScanData&xnat:imageScanData/series_class=%s" %
    #     (sessionId, scanId, label))
    # url = ("/data/experiments/%s/scans/%s?xsiType=xnat:ctScanData&type=%s" % (sessionId, scanId, label))
    encoded_label = urllib.parse.quote(label, safe='')
    url =f"/data/experiments/{sessionId}/scans/{scanId}?xsiType=xnat:ctScanData&type={encoded_label}"
    # #xnatSession.renew_httpsession()
    response = xnatSession.httpsess.put(xnatSession.host + url)
    if response.status_code == 200 or response.status_code == 201:
        print("Successfully set type for %s scan %s to '%s'" % (sessionId, scanId, label))
        # session_id=session_name=sessionId
        # scan_id=scan_name=scanId
        # try:
        #     insert_data(session_id, session_name, scan_id, scan_name)
        #
        #     # Update or create column
        #     column_name ="TESTING_INSERTION" #  "volume"  # Specify the new column name
        #     column_value ="YES" #  "200"  # Value to be set in the new column
        #     update_or_create_column_with_given_session_only(session_id, column_name, column_value)
        #
        #     # update_or_create_column(session_id, scan_id, column_name, column_value,session_name,scan_name)
        # except:
        #     pass
    else:
        errStr = "ERROR"
        if response.status_code == 403 or response.status_code == 404:
            errStr = "PERMISSION DENIED"
        raise Exception("%s attempting to set type for %s %s to '%s': %s" %
                        (errStr, sessionId, scanId, label, response.text))


if __name__ == '__main__':

    sessionDir = sys.argv[1]
    workingDir = sys.argv[2]
    sessionId = sys.argv[3]
    print ("Classifier_session_level.py sessionDir: {} workingDir: {} sessionId: {}".format (sessionDir, workingDir,sessionId))
    print ("XNAT_HOST: {} XNAT_USER: {} XNAT_PASS: {}".format(XNAT_HOST, XNAT_USER, XNAT_PASS))
    # print ("Classifier_session_level.py sessionDir: %, workingDir: %, sessionId: %" % (sessionDir, workingDir,sessionId))
    # print ("XNAT_HOST: %, XNAT_USER: %, XNAT_PASS: %" (XNAT_HOST, XNAT_USER, XNAT_PASS))
    ##############################################
    metadata_session=get_metadata_session(sessionId)
    for x in metadata_session:
        # if int(x['ID']) == scanId:
        scanId=x['ID']


        try:

            ###########################################################
            # xnatSesDir = sys.argv[4]
            # scans = [sys.argv[4]] #sys.argv[5].split()
            # scanId=scans[0]
            # Make working dirs
            rawDir = os.path.join(workingDir, 'RAW')
            os.makedirs(rawDir, exist_ok = True)
            jpgDir = os.path.join(workingDir, 'JPG' )
            os.makedirs(jpgDir, exist_ok = True)
            command="rm -r  " + rawDir + "/*"
            subprocess.call(command,shell=True)
            command="rm -r  " + jpgDir + "/*"
            subprocess.call(command,shell=True)
            command="rm -r /NIFTIFILEDIR/*"
            subprocess.call(command,shell=True)
            # for x in range(1,5):
            #     print(sys.argv[x])
            command="rm -r /ZIPFILEDIR/*"
            subprocess.call(command,shell=True)
            command="rm -r /DICOMFILEDIR/*"
            subprocess.call(command,shell=True)
            # for x in range(10):
            #     print("{}:XNAT_HOST".format(XNAT_HOST))
            #xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
            run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession)
            # Handle DICOM files that are not stored in a directory matching their XNAT scanId
            #xnatSession.close_httpsession()
        except Exception as e: # work on python 3.x
            print('Exception occured: '+ str(e))
            continue
