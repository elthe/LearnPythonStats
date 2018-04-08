#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数字图片的训练和识别。
参考代码：https://github.com/LiuXiaolong19920720/opencv-soduko
模块安装：pip install opencv-python
"""

import glob as gb
import cv2

## 获取numbers文件夹下所有文件路径
img_path = gb.glob("./images/numbers/*")

k = 0
labels = []
samples = []

## 对每一张图片进行处理
for path in img_path:
    # 读取图片
    img = cv2.imread(path)
    # 颜色空间转换（转换成灰度图）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯模糊
    # 这里(5, 5)表示高斯矩阵的长与宽都是5，标准差取0时OpenCV会根据高斯矩阵的尺寸自己计算。
    # 概括地讲，高斯矩阵的尺寸越大，标准差越大，处理过的图像模糊程度越大。
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 自适应阈值可以看成一种局部性的阈值，通过规定一个区域大小，
    # 比较这个点与区域大小里面像素点的平均值（或者其他特征）
    # 的大小关系确定这个像素点是属于黑或者白（如果是二值情况）
    # 参数说明：
    #   第一个原始图像
    #   第二个像素值上限
    #   第三个自适应方法Adaptive Method:
    #       — cv2.ADAPTIVE_THRESH_MEAN_C ：领域内均值
    #       — cv2.ADAPTIVE_THRESH_GAUSSIAN_C ：领域内像素点加权和，权 重为一个高斯窗口
    #   第四个值的赋值方法：只有cv2.THRESH_BINARY 和cv2.THRESH_BINARY_INV
    #   第五个Block size:规定领域大小（一个正方形的领域）
    #   第六个常数C，阈值等于均值或者加权值减去这个常数（为0相当于阈值 就是求得领域内均值或者加权值）
    #   这种方法理论上得到的效果更好，相当于在动态自适应的调整属于自己像素点的阈值，而不是整幅图像都用一个阈值。
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img,contours,-1,(0,0,255),3)
    height, width = img.shape[:2]
    # w = width/5
    ## 图片第一行和第二行数字
    list1 = []
    list2 = []
    for cnt in contours:
        # if cv2.contourArea(cnt)>100:
        [x, y, w, h] = cv2.boundingRect(cnt)

        if w > 30 and h > (height / 4):
            ## 按y坐标分行
            if y < (height / 2):
                list1.append([x, y, w, h])  ## 第一行
            else:
                list2.append([x, y, w, h])  ## 第二行
                # rect_list.append([x,y,w,h])
                # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                # cv2.imshow("number",img)
                # cv2.waitKey(200)

    ## 按x坐标排序，上面已经按y坐标分行
    list1_sorted = sorted(list1, key=lambda t: t[0])
    list2_sorted = sorted(list2, key=lambda t: t[0])
    # print list1
    # print list1_sorted
    # print len(list1)

    for i in range(5):
        [x1, y1, w1, h1] = list1_sorted[i]
        [x2, y2, w2, h2] = list2_sorted[i]
        ## 切割出每一个数字
        number_roi1 = gray[y1:y1 + h1, x1:x1 + w1]  # Cut the frame to size
        number_roi2 = gray[y2:y2 + h2, x2:x2 + w2]  # Cut the frame to size

        # number_roi1 = thresh[y1:y1+h1, x1:x1+w1] #Cut the frame to size
        # number_roi2 = thresh[y2:y2+h2, x2:x2+w2] #Cut the frame to size
        ## 对图片进行大小统一和预处理
        resized_roi1 = cv2.resize(number_roi1, (20, 40))
        thresh1 = cv2.adaptiveThreshold(resized_roi1, 255, 1, 1, 11, 2)

        resized_roi2 = cv2.resize(number_roi2, (20, 40))
        thresh2 = cv2.adaptiveThreshold(resized_roi2, 255, 1, 1, 11, 2)

        ## 每一个数字存入对应数字的文件夹
        number_path1 = "number\\%s\\%d" % (str(i + 1), k) + '.jpg'
        j = i + 6
        if j == 10:
            j = 0
        number_path2 = "number\\%s\\%d" % (str(j), k) + '.jpg'
        k += 1

        ## 归一化
        normalized_roi1 = thresh1 / 255.
        normalized_roi2 = thresh2 / 255.
        # cv2.imwrite(number_path1,number_roi1)
        # cv2.imwrite(number_path2,number_roi2)

        ## 把图片展开成一行，然后保存到samples
        ## 保存一个图片信息，保存一个对应的标签
        sample1 = normalized_roi1.reshape((1, 800))
        samples.append(sample1[0])
        labels.append(float(i + 1))

        sample2 = normalized_roi2.reshape((1, 800))
        samples.append(sample2[0])
        labels.append(float(j))

        cv2.imwrite(number_path1, thresh1)
        cv2.imwrite(number_path2, thresh2)
        cv2.imshow("number", normalized_roi1)
        cv2.waitKey(5)

# print sample1
## 这里才引入numpy是因为前面引入的话会自动把所有的list编程np.array
## 感觉array的append没有list的好用...
import numpy as np

## 这里还是把它们保存成了np.array...
samples = np.array(samples, np.float32)
# samples = samples.reshape((samples.size,1))
labels = np.array(labels, np.float32)
labels = labels.reshape((labels.size, 1))

np.save('./cache/cv_samples.npy', samples)
np.save('./cache/cv_label.npy', labels)

## 训练knn模型
samples = np.load('./cache/cv_samples.npy')
labels = np.load('./cache/cv_label.npy')

k = 80
train_label = labels[:k]
train_input = samples[:k]
test_input = samples[k:]
test_label = labels[k:]

model = cv2.ml.KNearest_create()
model.train(train_input, cv2.ml.ROW_SAMPLE, train_label)

# retval, results, neigh_resp, dists = model.findNearest(test_input, 1)
# string = results.ravel()
# print(string)
# print(test_label.reshape(1,len(test_label))[0])

img = cv2.imread('./images/cv_test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
## 阈值分割
ret, thresh = cv2.threshold(gray, 200, 255, 1)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
dilated = cv2.dilate(thresh, kernel)

## 轮廓提取
image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

##　提取八十一个小方格
boxes = []
for i in range(len(hierarchy[0])):
    if hierarchy[0][i][3] == 0:
        boxes.append(hierarchy[0][i])

height, width = img.shape[:2]
box_h = height / 9
box_w = width / 9
number_boxes = []
## 数独初始化为零阵
soduko = np.zeros((9, 9), np.int32)

for j in range(len(boxes)):
    if boxes[j][2] != -1:
        # number_boxes.append(boxes[j])
        x, y, w, h = cv2.boundingRect(contours[boxes[j][2]])
        number_boxes.append([x, y, w, h])
        # img = cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(0,0,255),2)
        # img = cv2.drawContours(img, contours, boxes[j][2], (0,255,0), 1)
        ## 对提取的数字进行处理
        number_roi = gray[y:y + h, x:x + w]
        ## 统一大小
        resized_roi = cv2.resize(number_roi, (20, 40))
        thresh1 = cv2.adaptiveThreshold(resized_roi, 255, 1, 1, 11, 2)
        ## 归一化像素值
        normalized_roi = thresh1 / 255.

        ## 展开成一行让knn识别
        sample1 = normalized_roi.reshape((1, 800))
        sample1 = np.array(sample1, np.float32)

        ## knn识别
        retval, results, neigh_resp, dists = model.findNearest(sample1, 1)
        number = int(results.ravel()[0])

        ## 识别结果展示
        cv2.putText(img, str(number), (x + w + 1, y + h - 20), 3, 2., (255, 0, 0), 2, cv2.LINE_AA)

        ## 求在矩阵中的位置
        soduko[int(y / box_h)][int(x / box_w)] = number

        # print(number)
        cv2.namedWindow("img", cv2.WINDOW_NORMAL);
        cv2.imshow("img", img)
        cv2.waitKey(30)

print("\n生成的数独\n")
print(soduko)
