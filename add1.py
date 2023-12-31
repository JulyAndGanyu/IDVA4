import os
import numpy as np
import cv2
path = '/home/gyh/output/cam/4/'
from scipy.ndimage import filters

for j in range(0,600):
    data = np.zeros((52,52),dtype=float)
    cam_car = np.zeros((52,52),dtype=float)
    cam_truck = np.zeros((52,52),dtype=float)
    cam_bus = np.zeros((52,52),dtype=float)
    path_car = path + str(j) +'-2.txt'

    path_trafficlight = path + str(j) +'-9.txt'
    path_bus = path + str(j) +'-7.txt'
    path_truck = path + str(j) +'-5.txt'
    path_person = path + str(j) +'-0.txt'
    path_bicycle = path + str(j) +'-1.txt'
    path_motorcycle = path + str(j) +'-3.txt'
    if(os.path.exists(path_car)):
        cam_car = np.loadtxt(path_car,dtype=float,delimiter =' ')
        cam_car = filters.gaussian_filter(cam_car, 2)
        #data = np.add(data,cam_car)
        cam_car = cam_car.flatten()
    else:
        cam_car = np.zeros(2704)
    if(os.path.exists(path_bus)):
        cam_bus = np.loadtxt(path_bus,dtype=float,delimiter =' ')
        cam_bus = filters.gaussian_filter(cam_bus, 2)
     #   data = np.add(data,cam_bus)
        cam_bus = cam_bus.flatten()
    else:
        cam_bus = np.zeros(2704)
        
    if(os.path.exists(path_truck)):
        cam_truck = np.loadtxt(path_truck,dtype=float,delimiter =' ')
        cam_truck = filters.gaussian_filter(cam_truck, 4)
        cam_truck = cam_truck.flatten()
    else:
        cam_truck = np.zeros(2704)     


                                                         
        
    if(os.path.exists(path_trafficlight)):
        cam_trafficlight = np.loadtxt(path_trafficlight,dtype=float,delimiter =' ')
        #data = np.add(data,cam_trafficlight)
        cam_trafficlight = filters.gaussian_filter(cam_trafficlight, 2)
        cam_trafficlight = cam_trafficlight.flatten()
        
    else:
        cam_trafficlight = np.zeros(2704)    


    if(os.path.exists(path_person)):
        cam_person = np.loadtxt(path_person,dtype=float,delimiter =' ')
        cam_person = filters.gaussian_filter(cam_person, 2)
        #data = np.add(data,cam_person)
        cam_person = cam_person.flatten()
    else:
        cam_person = np.zeros(2704)
        
    if(os.path.exists(path_bicycle)):
        cam_bicycle = np.loadtxt(path_bicycle,dtype=float,delimiter =' ')
        cam_bicycle = filters.gaussian_filter(cam_bicycle, 2)
        #data = np.add(data,cam_bicycle)
        cam_bicycle = cam_bicycle.flatten()           
    else:
        cam_bicycle = np.zeros(2704)


 
    if(os.path.exists(path_motorcycle)):
        cam_motorcycle = np.loadtxt(path_motorcycle,dtype=float,delimiter =' ')
        cam_motorcycle = filters.gaussian_filter(cam_motorcycle, 2)
        #data = np.add(data,cam_motorcycle)
        cam_motorcycle = cam_motorcycle.flatten()        
    else:
        cam_motorcycle = np.zeros(2704)


    data = data.flatten()
    
    print(j)
    straight = np.loadtxt('/home/gyh/straight.txt')
    right = np.loadtxt('/home/gyh/right.txt')
    left = np.loadtxt('/home/gyh/left.txt')
    straight =straight.flatten()
    right =right.flatten()
    left =left.flatten()
    for i in range (data.shape[0]):
        #num =int(cam_motorcycle[i]>0.39)+int(cam_bicycle[i]>0.39)+int(cam_person[i]>0.39)+int(cam_trafficlight[i]>0.39)+int(cam_bus[i]>0.39)+int(cam_car[i]>0.39)+int(cam_truck[i]>0.39)
        #num =int(cam_motorcycle[i]>0.39)+int(cam_bicycle[i]>0.39)+int(cam_bus[i]>0.39)+int(cam_car[i]>0.39)+int(cam_truck[i]>0.39)
        #num=1 if num==0 else num
        #data[i] = (data[i]+cam_motorcycle[i]+cam_bicycle[i]+cam_person[i]+cam_trafficlight[i]+cam_bus[i]+cam_car[i]+cam_truck[i])/num
        data[i] = data[i]+cam_motorcycle[i]+cam_bicycle[i]+cam_person[i]+cam_trafficlight[i]+cam_bus[i]+cam_car[i]+cam_truck[i]+cam_trafficlight[i]
        #data[i] = data[i] + cam_person[i]
        #data[i] = data[i]+cam_person[i]
        #data[i] = (data[i]+cam_motorcycle[i]+cam_bicycle[i]+cam_bus[i]+cam_car[i]+cam_truck[i])/num   
        #print(num)
        #data[i] = cam_car[i]
        #    data[i] = data[i]* right[i]
        #if j>230:
       #     data[i] = data[i]* straight[i]
            #data[i] = data[i]* straight[i]
       #if j>45 and j<164:
       
        data[i] = data[i] * (straight[i]**0.2)
        #if j>164 and j<300:
         #   data[i] = data[i]* left[i]
        #if j>265:
        #    data[i] = data[i]* straight[i]        
    data = data.reshape(52,52) 
    data = data.astype('float32')  
    #print(data)
    #data = cv2.resize(data, (180, 320),interpolation=cv2.INTER_CUBIC)   
    
    #for i in range (0,52):
    #    print(right[i])
    
    #if i<150:
    #data =data*straight
    #else:
    #    data = data* right
    
    np.savetxt("/home/gyh/output/all/4/" +("%s"% j)+ (".txt" ), data,fmt='%.5f')
    
