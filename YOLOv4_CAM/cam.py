import colorsys
import os

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
from PIL import Image, ImageDraw, ImageFont
from torch.autograd import Variable

from nets.yolo4 import YoloBody
from utils.utils import (DecodeBox, bbox_iou, letterbox_image,
                         non_max_suppression, yolo_correct_boxes)



class YOLO(object):
    _defaults = {
        "model_path"        : 'model_data/yolo4_weights.pth',
        "anchors_path"      : 'model_data/yolo_anchors.txt',
        "classes_path"      : 'model_data/coco_classes.txt',
        "model_image_size"  : (416, 416, 3),
        "confidence"        : 0.5,
        "iou"               : 0.3,
        "cuda"              : False,

        "letterbox_image"   : False,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #---------------------------------------------------#

    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.generate()


    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names
    

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape([-1, 3, 2])[::-1,:,:]


    def generate(self):

 
        self.net = YoloBody(len(self.anchors[0]), len(self.class_names)).eval()


        print('Loading weights into state dict...')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        state_dict = torch.load(self.model_path, map_location=device)
        self.net.load_state_dict(state_dict)
        print('Finished!')
        
        if self.cuda:
            os.environ["CUDA_VISIBLE_DEVICES"] = '0'
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()


        self.yolo_decodes = []
        for i in range(3):
            self.yolo_decodes.append(DecodeBox(self.anchors[i], len(self.class_names),  (self.model_image_size[1], self.model_image_size[0])))


        print('{} model, anchors, and classes loaded.'.format(self.model_path))

        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))


    def detect_image(self, image,output_labels,id_class):
        image_shape = np.array(np.shape(image)[0:2])


        if self.letterbox_image:
            crop_img = np.array(letterbox_image(image, (self.model_image_size[1],self.model_image_size[0])))
        else:
            crop_img = image.convert('RGB')
            crop_img = crop_img.resize((self.model_image_size[1],self.model_image_size[0]), Image.BICUBIC)
        photo = np.array(crop_img,dtype = np.float32) / 255.0
        photo = np.transpose(photo, (2, 0, 1))

        images = [photo]

        with torch.no_grad():
            images = torch.from_numpy(np.asarray(images))
            if self.cuda:
                images = images.cuda()


            outputs = self.net(images)
            output_list = []
            for i in range(3):
                output_list.append(self.yolo_decodes[i](outputs[i]))
                
            results = non_max_suppression(torch.cat(output_list, 1), num_classes=80)
            print(results)
            print(results[0] is None)
            if results[0] is None is None:
             
                top_label =  0
                top_conf  = 0.0
            else:
                top_label   = np.array(results[0][:, 6], dtype = 'int32')
                top_conf    = results[0][:, 4] * results[0][:, 5]
            
                for i, c in list(enumerate(top_label)):
                    predicted_class = self.class_names[int(c)]
                    score           = str(top_conf[i].item())
                    if float(score) > 0.55:
                    
                        id_class.append(int(c))
                
                    if predicted_class not in self.class_names:
                        continue
                    write_path = output_labels.split('.')[0] +".txt"
                    print(write_path)
                    with open(write_path,"a") as f:
                        f.write("%s %s %s \n" % (c,predicted_class, score[:6] ))
            
            
        return output_list


def show_CAM(image_path, feature_maps, class_id, all_cam_add,all_ids=85, show_one_layer=False):
            """
            feature_maps: this is a list [tensor,tensor,tensor], tensor shape is [1, 3, N, N, all_ids]
            """
            
            SHOW_NAME = ["class_score"]
            img_ori = cv2.imread(image_path)
            layers0 = feature_maps[0].reshape([-1, all_ids])
            #print(layers0.shape)
            layers1 = feature_maps[1].reshape([-1, all_ids])
            layers2 = feature_maps[2].reshape([-1, all_ids])
            layers = torch.cat([layers0, layers1, layers2], 0)
            score_max_v = layers[:, 4].max()  # compute max of score from all anchor
            score_min_v = layers[:, 4].min()  # compute min of score from all anchor
            class_max_v = layers[:, 5 + class_id].max()  # compute max of class from all anchor
            class_min_v = layers[:, 5 + class_id].min()  # compute min of class from all anchor
            all_ret = [[],[],[]]

            for j in range(3):  # layers
                layer_one = feature_maps[j]
                # compute max of score from three anchor of the layer[0]
                anchors_score_max = layer_one[0, ..., 4].max(0)[0]
                
                # compute max of class from three anchor of the layer
                anchors_class_max = layer_one[0, ..., 5 + class_id].max(0)[0]
 
                scores = ((anchors_score_max - score_min_v) / (
                        score_max_v))
                classes = ((anchors_class_max - class_min_v) / (
                        class_max_v))
                layer_one_list = []
                layer_one_list.append(scores*classes)
                for idx, one in enumerate(layer_one_list):
                    layer_one = one.cpu().numpy()
                    #ret = ((layer_one - layer_one.min()) / (layer_one.max())) * 255
                    ret = ((layer_one - layer_one.min()) / (layer_one.max())) 
                    #ret = ret.astype(np.uint8)
                    all_ret[j].append(cv2.resize(ret, (52, 52)).copy())
                
            cam_1 = (np.array(all_ret[0])).flatten()
            #for i in range(cam_1.shape[0]):
            #    print(cam_1[i])
            cam_2 = (np.array(all_ret[1])).flatten()
     
            cam_3 = (np.array(all_ret[2])).flatten()
            cam = cam_2.reshape(52,52)
            if class_id == 0:
                cam = cam_2.reshape(52,52) 
            if class_id == 1:
                cam = cam_2.reshape(52,52)   
            if class_id == 2:
                cam = np.zeros(2704).astype("float32")
                for i in range(cam_2.shape[0]):
                    #print(i)
                    num =int(cam_2[i]>0.39)+int(cam_3[i]>0.39)
                    num=1 if num==0 else num
                    #print(num)
                    cam[i] = (cam_2[i]+cam_3[i])/num
                    #cam[i] =cam_3[i]
                cam =cam.reshape(52,52)
            if class_id == 7:
                cam = np.zeros(2704).astype("float32")
                for i in range(cam_2.shape[0]):
                    #print(i)
                    num =int(cam_2[i]>0.39)+int(cam_3[i]>0.39)
                    num=1 if num==0 else num
                    #print(num)
                    cam[i] = (cam_2[i]+cam_3[i])/num
                    #cam[i] =cam_3[i]
                cam =cam.reshape(52,52)
            if class_id == 9:
                cam = cam_3.reshape(52,52)
                
            gray=cam.squeeze()
            id_name = (image_path.split('.')[0]).split('/')[-1]
            np.savetxt("/home/gyh/output/cam/4/" +("%d-"% int(id_name))+ ("%d.txt" % class_id), gray,fmt='%.5f')
            gray = gray.astype(np.uint8)
            
            #np.savetxt("/media/gyh/WNPP/cam-output2/9/cam/" +("%d-"% int(id_name))+ ("%d.txt" % class_id), gray,fmt='%d')
           # all_cam_add = all_cam_add + gray
           # gray = gray[:, :, None]   
           # cam = cv2.resize(gray, (img_ori.shape[1], img_ori.shape[0]))
            #cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
           # show = cam * 0.5 + img_ori * 0.5
            #show = show.astype(np.uint8)
           # cv2.imshow(f"one_{SHOW_NAME[idx]}", show)
           # cv2.waitKey(0)
stride = [13,26,52]
yolo = YOLO()
output_label ="/home/gyh/output/4/"
path = "/home/gyh/tupian/4/"
img_path = os.listdir(path)
for i in img_path:
    ret = []
    final_path = path + i
    image = Image.open(final_path)
    output_labels =  output_label+i
    id_class = []
    set_ids = []
    all_cam_add = np.zeros((52,52),dtype=int)
    output_list = yolo.detect_image(image,output_labels,id_class)
    for i,f in enumerate(output_list):
        ret.append(f.reshape(1,3,stride[i],stride[i],85))
    for ids in id_class:
        if ids not in set_ids:
            set_ids.append(ids)
    for idx in set_ids:
        if idx== 0 or idx== 1 or idx ==2 or idx==3 or idx==5 or idx==7 or idx==9 or idx==11:
        #if idx==2:
            show_CAM(final_path, ret, idx,all_cam_add)
    #np.savetxt("/media/c/WNPP/cam_output/output/" +("%s-"%i)+ ("%d.txt"), all_cam_add,fmt='%d')
    #ret.append(f.reshape(1,3,stride[i],stride[i],85))
    #show_CAM(final_path, ret, 2)
    #for i,f in enumerate(output_list):
#image = Image.open(path)
#output_list = yolo.detect_image(image)
#for i,f in enumerate(output_list):
#    ret.append(f.reshape(1,3,stride[i],stride[i],85))


#show_CAM(path, ret, 2)
