import os
import cv2

def convert_images(num_bands, path, write_path, conn):
    labels_index = os.listdir(path)
    for label in labels_index:
        images_files = os.listdir(path + '/' + str(label))

        count = 0
        for i in range(int(len(images_files)/num_bands)):
            img1 = cv2.imread(path + '/' + label + '/' + images_files[count], cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(path + '/' + label + '/' + images_files[count+1], cv2.IMREAD_GRAYSCALE)
            img3 = cv2.imread(path + '/' + label + '/' + images_files[count+2], cv2.IMREAD_GRAYSCALE)
            count+=num_bands
            cv2.imwrite(write_path + '/' + label + '/' + conn + str(i) + '.png', cv2.merge((img1, img2, img3)))

    
    

#=================================================   
conn = 'squared_coherence'
window = '1-seg'
convert_images(3, 'IMG/'+ window + '/' + conn, 'IMG_Bands/'+ window +'/' + conn, conn + '-' + window)
    
    
        
        
    