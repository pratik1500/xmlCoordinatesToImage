import glob
import os
import xmltodict
import json
import pprint
import cv2
from PIL import Image


# Printing results
pp = pprint.PrettyPrinter(indent=4)


# Look for XML files and parses then as if they were Pascal VOC Files
def process(filename):
    # Finds all XML files on data/ and append to list
    pascal_voc_contents = []
    os.chdir("data")

    print("Found {} files in data directory!".format(
        str(len(glob.glob(filename+".xml")))))
    for file in glob.glob(filename+".xml"):
        f_handle = open(file, 'r')
        print("Parsing file '{}'...".format(file))
        pascal_voc_contents.append(xmltodict.parse(f_handle.read()))

    # Process each file individually
    for index in pascal_voc_contents:
        image_file = index['annotation']['filename']
        # If there's a corresponding file in the folder,
        # process the images and save to output folder
        if os.path.isfile(image_file):
           path=  extractDataset(index['annotation'],filename)
           return path
        else:
            return "something gone wrong"


# Extract image samples and save to output dir
def extractDataset(dataset,filename):
    print("Found {} objects on image '{}'...".format(
        len(dataset['object']), dataset['filename']))

    # Open image and get ready to process
    img = Image.open(dataset['filename'])

    # Create output directory
    save_dir = dataset['filename'].split('.')[0]
    try:
        os.mkdir(save_dir)
    except:
        pass
    # Image name preamble
    sample_preamble = save_dir + "/" + dataset['filename'].split('.')[0] + "_"
    # Image counter
    i = 0
    window_name = 'Image'
    color = (255, 0, 0)
    thickness = 2
    
    img = cv2.imread(dataset['filename'])
    # Run through each item and save cut image to output folder
    for item in dataset['object']:
        # Convert str to integers
        bndbox = dict([(a, int(b)) for (a, b) in item['bndbox'].items()])
        # Save
        im = cv2.rectangle(img, (bndbox['xmin'],bndbox['ymin']), (bndbox['xmax'],bndbox['ymax']), color, thickness)
        # im = cv2.rectangle(img, (117,237), (274,517), color, thickness)
        cv2.putText(im, item['name'], (bndbox['xmin'], bndbox['ymin']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        # cv2.imshow(window_name, im) 
        # filename ='savedImage.jpg'
        filename= filename+'.jpg'
        # Using cv2.imwrite() method
        # Saving the image
        
        i = i + 1
    directory =r"D:\PascalVOC-to-Images\static"
    os.chdir(directory)
    cv2.imwrite(filename, img)
    return filename



