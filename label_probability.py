import os, sys, errno
import math
import scipy.misc
import png
import tensorflow as tf
import re
import glob
from collections import Counter
from itertools import repeat, chain
import warnings
import pydicom as dicom
import numpy as np

def predictFromPixelData(image, basename, jpgDir):
    # Save as jpg
    jpgFile = os.path.join(jpgDir, basename + ".png")
    print("Converting dcm to %s" % jpgFile)
    shap = image.shape
    image_2d = image.astype(float)
    image_2d_scaled = np.uint8((np.maximum(image_2d,0) / image_2d.max()) * 255.0)
    with open(jpgFile, 'wb') as png_file:
            w = png.Writer(shap[1], shap[0], greyscale=True)
            w.write(png_file, image_2d_scaled)  
      
    # Unpersists graph from file
    with tf.gfile.FastGFile("/software1/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Read in the image_data
    jpgFileData = tf.gfile.FastGFile(jpgFile, 'rb').read()
    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': jpgFileData})
        prediction = (-predictions[0]).argsort()[:2]
    labels = [line.rstrip() for line in tf.gfile.GFile("/software1/retrained_labels.txt")]
    labelP = []
    for i in range(2):
        labelP.append(labels[prediction[i]])

    print("Pixel-based classification is %s" % ' '.join(labelP))
    return labelP


# def predictFromDcmHeader(ds, nDicomFiles, labelPIsEmpty):
#     #classification based on dicom header
#     try:
#         seriesDesc=str(ds.SeriesDescription).lower().replace("image","")
#     except (AttributeError, IndexError) as err:
#         seriesDesc="NA"

#     try:
#         angio=str(ds.AngioFlag).lower()
#     except (AttributeError, IndexError) as err:
#         angio="NA"
    
#     labelH=[]
#     if (any(x in seriesDesc for x in ['scout'])):
#         labelH.append('Scout')
#     if (((seriesDesc.find("loc") != -1) and (seriesDesc.find("block") == -1) and (seriesDesc.find("location") == -1)) or (nDicomFiles <= 3 and labelPIsEmpty)):
#         labelH.append('Localizer')
    # if (any(x in seriesDesc for x in ['flash','ge','gre']) and seriesDesc.find("average") == -1 and seriesDesc.find("mprage") == -1):
    #     labelH.append('FLASH')
    # if any(x in seriesDesc for x in ['dif','dwi','dti','dbsi','tracew','colfa','tensor','fa','adc','resolve','ansio','aniso','iso']):
    #     labelH.append('DWI')
    # if any(x in seriesDesc for x in ['swi','swan']):
    #     labelH.append('SWI')
    # if ((seriesDesc.find("t2") != -1) and ((seriesDesc.find("*") != -1) or (seriesDesc.find("star") != -1))):
    #     labelH.append('T2star')
    # if any(x in seriesDesc for x in ['bold','fmri','rest']):
    #     labelH.append('Bold')
    # if any(x in seriesDesc for x in ['asl']):
    #     labelH.append('ASL')
    # if any(x in seriesDesc for x in ['dsc','dce','perf']):
    #     labelH.append('Perfusion')
    # if (any(x in seriesDesc for x in ['angio','tof','exorcist','tumbler']) or angio=='y'):
    #     labelH.append('Angio')
    # if (any(x in seriesDesc for x in ['mip'])):
    #     labelH.append('minIP')
    # if any(x in seriesDesc for x in ['tse','fse']):
    #     labelH.append('TSE')
    # if any(x in seriesDesc for x in ['flair']):
    #     labelH.append('Flair')
    # if (seriesDesc.find("map") != -1) and (seriesDesc.find("field") != -1):
    #     labelH.append('Fieldmap')
    # if (any(x in seriesDesc for x in ['mag'])):
    #     labelH.append('part-Mag_GRE')
    # if (any(x in seriesDesc for x in ['pha'])):
    #     labelH.append('part-Phase_GRE')
    # if (any(x in seriesDesc for x in ['t1','mpr','fspgr']) and (seriesDesc.find("t2") == -1) and (not any(x in seriesDesc for x in ['t10','t11','t12','t13','t14','t15','t16','t17','t18','t19']))):
    #     labelH.append('T1w')
    # if (any(x in seriesDesc for x in ['t2']) and (not any(x in seriesDesc for x in ['t20','t21','t22','t23','t24','t25','t26','t27','t28','t29']))):
    #     labelH.append('T2w')

    # print("Header-based classification is %s" % ' '.join(labelH))
    # return labelH
    

def combineClassifications(ds, labelP,nDicomFiles):
    # extract window width, series description and image type
    try:
        Window_Width=int(re.findall(r'\d+', str(ds.WindowWidth).split(",")[0])[0])
    except (AttributeError, IndexError) as err:
        Window_Width="NAN"
    try:
        Series_Description=ds.SeriesDescription.lower()
    except (AttributeError, IndexError) as err:
        Series_Description="NAN"
    try:
        ImageType=str(ds.ImageType).lower()
    except (AttributeError, IndexError) as err:
        ImageType="NAN"
    

    # exctact Slice Thicness
    try:
        Slice_Thickness=int(re.findall(r'\d+', str(ds.SliceThickness).split(",")[0])[0])
    except (AttributeError, IndexError) as err:
        Slice_Thickness="NAN"


    # calculate final label
    if (len(labelP)==0 or nDicomFiles<10):
        print('1')
        overallLabel = "Other"
    elif (Series_Description.find("brain") != -1 and Series_Description.find("bone") == -1 and Series_Description.find("ang") == -1 and Series_Description.find("perf") == -1 and Series_Description.find("cor") == -1 and Series_Description.find("sag") == -1):
        overallLabel="Z-Axial-Brain"
    elif (Series_Description.find("bone") != -1):
        overallLabel="Z-Axial-Bone"
    elif ((Series_Description.find("ang") != -1 and Series_Description.find("angeled") == -1) or (Series_Description.find("ctp") != -1)):
        print('2')
        overallLabel="Other"
    elif ((Series_Description.find("perf") != -1) or (Series_Description.find("cta") != -1)):
        print('3')
        overallLabel="Other"
    elif ((Series_Description.find("cor") != -1) or (Series_Description.find("sag") != -1) or (Series_Description.find("art") != -1) or (Series_Description.find("smart") != -1) or (Series_Description.find("chest") != -1) or (Series_Description.find("lung") != -1) or (Series_Description.find("monitor") != -1) or (Series_Description.find("pelvis") != -1) or (Series_Description.find("pe") != -1) or (Series_Description.find("spine") != -1) or (Series_Description.find("skull") != -1)):
        print('4')
        overallLabel="Other"
    else:
        if ((labelP[0]=="Z-Brain-Thin" or labelP[1]=="Z-Brain-Thin" or labelP[0]=="Z-Axial-Bone" or labelP[1]=="Z-Axial-Bone" or labelP[0]=="Z-Axial-Brain" or labelP[1]=="Z-Axial-Brain" or Series_Description.find("head") != -1) and ImageType.find("axial") != -1 and ImageType.find("derived") == -1):
            if(Slice_Thickness=="NAN"):
                print('5')
                overallLabel = "Other"
            else:
                if (Window_Width>=800 and Slice_Thickness>=1 and Slice_Thickness<=6):
                    overallLabel="Z-Axial-Bone"
                elif (Slice_Thickness>=1 and Slice_Thickness<3 and Window_Width<1000 ):
                    overallLabel="Z-Brain-Thin"
                elif ((Slice_Thickness>=3 and Slice_Thickness<=10) and (Window_Width<800)):
                    overallLabel="Z-Axial-Brain"
                else:
                    print('6')
                    overallLabel = "Other"
        else:
            print('7')
            overallLabel = "Other"
    print("Window_Width is ", str(Window_Width))
    print("Slice_Thickness is ", str(Slice_Thickness))
    print("Series_Description is ", str(Series_Description))
    print("ImageType is ", str(ImageType)) 
    print("overallLabel is ", str(overallLabel))

    return overallLabel


def getContrastLabel(ds):
# detect contrast based on dicom header 
    try:
        ContrastBolusAgent=ds.ContrastBolusAgent
    except (AttributeError, IndexError) as err:
        ContrastBolusAgent="NAN"
    try:
        Volume=ds.ContrastBolusVolume
    except (AttributeError, IndexError, KeyError) as err:
        Volume="NAN"
    if (ContrastBolusAgent!="NAN"):
        if (Volume!="NAN"):
            if(Volume==0):
                contrast=""
            else:
                contrast="CE_"
        else:
            if(len(ContrastBolusAgent)!=0):
                contrast="CE_"
            else:
                contrast=""
    else:
        contrast=""

    print("contrast is ", str(contrast))
    return contrast



def classify(dcmFile, jpgDir, scanId, nDicomFiles):
    # Read DICOM
#     ds = dicom.read_file(dcmFile)
    ds = dicom.dcmread(dcmFile)

    try:
        modality=str(ds.Modality).lower()
    except:
        modality="NA"
    
    finalLabel = 'Unknown'
    if not "ct" in modality:
        print("%s is not an CT scan, classifying as '%s'" % (scanId, finalLabel))
    else:
        #Image classification
        try:
            imageType=str(ds.ImageType).lower()
        except (AttributeError, IndexError) as err:
            imageType="NA"
    
        if "primary" in imageType and not "derived" in imageType:
            # classification based on pixel info
            labelP = predictFromPixelData(ds.pixel_array, os.path.splitext(os.path.basename(dcmFile))[0], jpgDir)
            # Combine
            overallLabel = combineClassifications(ds, labelP,nDicomFiles)
            if (overallLabel=="Z-Axial-Bone" or overallLabel=="Z-Brain-Thin" or overallLabel=="Z-Axial-Brain"):
                finalLabel = getContrastLabel(ds) + overallLabel
            else:
                finalLabel=overallLabel
        else:
            finalLabel = "Other"
            print("%s has ImageType='Derived', classifying as '%s'" % (scanId, finalLabel))

    return finalLabel
