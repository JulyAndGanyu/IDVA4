clear all;close all;clc;

folder1 = 'D:\saliency_eval\mlnet\2';
folder2 = 'D:\saliency_eval\gt\2';
files1 = dir(fullfile(folder1,'*.txt'));
files2 = dir(fullfile(folder2,'*.txt'));
CC_ = 0
KL_ = 0
NSS_ = 0
SIM_ = 0
AUC_B = 0
AUC_J = 0
for i = 1:length(files1)
    file1 = fullfile(folder1,files1(i).name);
    file2 = fullfile(folder2,files2(i).name);
    temp = load(file1);
    data2 = load(file2);
    data1 = imresize(temp, size(data2))
    data1 =  data1 -min(data1(:));
    data1 =  data1/max(data1(:));
    CC_ = CC_ + CC(data1,data2)
    KL_ = KL_ + KLdiv(data1,data2)
    NSS_ =NSS_ + NSS(data1,data2)
    SIM_ = SIM_ + similarity(data1,data2)
    AUC_B = AUC_B + AUC_Borji(data1,data2)
    AUC_J = AUC_J + AUC_Judd(data1,data2)
end