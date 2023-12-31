import cv2
import glob
import os

def video_to_frame(save_path,video_path):
    video = cv2.VideoCapture(video_path)
    index = 0
    if video.isOpened():
        rval,frame = video.read()
    else:
        rval = False
    while rval:
        print(index)
        rvall,frame = video.read()
        cv2.imwrite(save_path + '/'+str(index) + '.jpg',frame)
        index+=1

if __name__ =="__main__":
    video_to_frame(video_path="/media/c/316C-664B/sp/4.mp4",save_path="/media/c/316C-664B/app/4")
    print("succeed")
