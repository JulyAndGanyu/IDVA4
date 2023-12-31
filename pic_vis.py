import cv2
import numpy as np


cam_root = '/home/gyh/output/all/4/'
img_root = '/home/gyh/tupian/4/'
for i in range(0,500):
    cam_path = cam_root + str(i) +'.txt'
    img_path = img_root + str(i) +'.jpg'
    cam = np.loadtxt(cam_path,dtype=float,delimiter =' ')
    cam = cam-cam.min()
    cam = cam/cam.max() *255
    img = cv2.imread(img_path)
    gray = cam.astype('float32')
    cam_1 = cv2.resize(cam, (img.shape[1], img.shape[0]),interpolation=cv2.INTER_CUBIC) 
    
    #cam_1 = cv2.resize(cam, (img.shape[1], img.shape[0]))   
    gray = cam_1.astype(np.uint8) 
    cam = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    show = cam * 0.5 + img * 0.5
    show = show.astype(np.uint8)
    cv2.imshow("0", show)
    cv2.imwrite('/home/gyh/output/saliency/2/'+str(i)+".jpg", show)
    cv2.waitKey(0)
