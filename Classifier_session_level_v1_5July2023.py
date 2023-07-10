#!/usr/bin/python

import os, sys, errno, shutil, uuid,json
import math
import glob
import re,argparse
import inspect
import pandas as pd
import requests
import pydicom as dicom
import subprocess
from xnatSession import XnatSession
import DecompressDCM,time
import label_probability
# Prep XNAT session
XNAT_HOST = 'https://snipr.wustl.edu' #os.environ['XNAT_HOST']#
XNAT_USER = os.environ['XNAT_USER']
XNAT_PASS = os.environ['XNAT_PASS']
catalogXmlRegex = re.compile(r'.*\.xml$')

def wait_for_file_tobe_written(file_path,time_to_wait):
    # time_to_wait = 10
    time_counter = 0
    while not os.path.exists(file_path):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break
def get_slice_idx(nDicomFiles):
    return min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain
def get_metadata_session(sessionId):
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    return metadata_session
def call_get_metadata_session_saveascsv(args):
    sessionId=args.stuff[1]
    filename=args.stuff[2]
    get_metadata_session_saveascsv(sessionId,filename)

def get_metadata_session_saveascsv(sessionId,filename):
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    df_scan = pd.read_json(json.dumps(metadata_session))
    df_scan.to_csv(filename,index=False)
    return metadata_session

def get_dicom_from_filesystem(sessionId, scanId,xnatSession):
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
    print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId, scanId))
    xnatSession.renew_httpsession()
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

def get_dicom_using_xnat(sessionId, scanId,xnatSession):
    # xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId,scanId ))
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)

    result = response.json()['ResultSet']['Result']
    nDicomFiles = len(result)
    if nDicomFiles == 0:
        raise Exception("No DICOM files for %s stored in XNAT" % scanId)

#     # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    print(selDicomAbs)
#     # selDicomAbs_split=selDicomAbs.split('/')
#     # print(selDicomAbs_split[-5]+'_'+selDicomAbs_split[-3])
#     ######################################################################################

#     # print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/resources/DICOM/files?format=zip" % 
        (sessionId, scanId))

    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    zipfilename=sessionId+scanId+'.zip'
    with open(zipfilename, "wb") as f:
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    command = 'unzip -d /ZIPFILEDIR ' + zipfilename
    subprocess.call(command,shell=True)

    command = 'cp  /ZIPFILEDIR/*/*/*/*/*/*/*.dcm  /DICOMFILEDIR/ '
    subprocess.call(command,shell=True)
#     #################################################################
    sessionDir='/DICOMFILEDIR'

    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
# #/ZIPFILEDIR/BJH_011_13102019_0715/*/*/*/*/**
    selDicom=os.path.join(sessionDir,os.path.basename(selDicomAbs))
    print(selDicom) 
    return selDicom, nDicomFiles

def run_classifier_7July_2023(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession):
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
    url = ("/data/experiments/%s/scans/%s?xsiType=xnat:ctScanData&type=%s" % (sessionId, scanId, label))
    # xnatSession.renew_httpsession()
    response = xnatSession.httpsess.put(xnatSession.host + url)
    if response.status_code == 200 or response.status_code == 201:
        print("Successfully set series_class for %s scan %s to '%s'" % (sessionId, scanId, label))
    else:
        errStr = "ERROR"
        if response.status_code == 403 or response.status_code == 404:
            errStr = "PERMISSION DENIED"
        raise Exception("%s attempting to set series_class for %s %s to '%s': %s" %
                        (errStr, sessionId, scanId, label, response.text))


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
    url = ("/data/experiments/%s/scans/%s?xsiType=xnat:ctScanData&type=%s" % (sessionId, scanId, label))
    # xnatSession.renew_httpsession()
    response = xnatSession.httpsess.put(xnatSession.host + url)
    if response.status_code == 200 or response.status_code == 201:
        print("Successfully set series_class for %s scan %s to '%s'" % (sessionId, scanId, label))
    else:
        errStr = "ERROR"
        if response.status_code == 403 or response.status_code == 404:
            errStr = "PERMISSION DENIED"
        raise Exception("%s attempting to set series_class for %s %s to '%s': %s" % 
            (errStr, sessionId, scanId, label, response.text))
def call_classifier_v1(args):
    return_value=0
    try:
        sessionDir = args.stuff[1]
        workingDir = args.stuff[2]
        sessionId = args.stuff[3]
        command = "echo  success at : " +  inspect.stack()[0][3]  + " >> " + "/workingoutput/error.txt"
        subprocess.call(command,shell=True)
        print("I SUCCEEDED AT ::{}".format(inspect.stack()[0][3]))
        classifier_v1(sessionDir,workingDir,sessionId)
    except Exception:
        command = "echo  FAILURE at : " +  inspect.stack()[0][3]  + " >> " + "/workingoutput/error.txt"
        subprocess.call(command,shell=True)
        command = "echo  ERROR : " +  Exception  + " >> " + "/workingoutput/error.txt"
        subprocess.call(command,shell=True)


    return 1
def classifier_v1(sessionDir,workingDir,sessionId):
    # sessionDir = sys.argv[1]
    # workingDir = sys.argv[2]
    # sessionId = sys.argv[3]
    ##############################################
    try:
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
                xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
                run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession)
                # Handle DICOM files that are not stored in a directory matching their XNAT scanId
                xnatSession.close_httpsession()
            except Exception as e: # work on python 3.x
                print('Exception occured: '+ str(e))
                continue
        command = "echo  SUCCESS at : " +  inspect.stack()[0][3]  + " >> " + "/workingoutput/error.txt"
        subprocess.call(command,shell=True)
    except Exception:
        command = "echo  FAILURE at : " +  inspect.stack()[0][3]  + " >> " + "/workingoutput/error.txt"
        subprocess.call(command,shell=True)
        command = "echo  ERROR : " +  Exception  + " >> " + "/workingoutput/error.txt"
        subprocess.call(command,shell=True)
def main():
    print("WO ZAI ::{}".format("main"))
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function == "call_classifier_v1":
        return_value=call_classifier_v1(args)
    return  return_value


if __name__ == '__main__':
    
    sessionDir = sys.argv[1]
    workingDir = sys.argv[2]
    sessionId = sys.argv[3]
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
            xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
            run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession)
            # Handle DICOM files that are not stored in a directory matching their XNAT scanId
            xnatSession.close_httpsession()
        except Exception as e: # work on python 3.x
            print('Exception occured: '+ str(e))
            continue 