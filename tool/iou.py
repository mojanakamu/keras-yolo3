import cv2
import numpy as np
import os
import csv
import xml.etree.ElementTree as ET

LOW_COLOR = np.array([255, 128, 128])
HIGH_COLOR = np.array([255, 128, 128])

test_data_path = '../' + 'data/test01/'
test_data_img_path = test_data_path + 'img/'
test_data_estimation_result_path = test_data_path + 'estimation/'

with open(test_data_estimation_result_path + 'estimation.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader) 

    for i,row in enumerate(reader):
        print('{0}:{1}'.format(i, row))

        #画像パス名から正解データのxmlパスを特定
        print('image_path:' + row[0])
        image_name_start_index = row[0].rfind('/')
        image_name_last_index = row[0].rfind('.')
        image_name =row[0][image_name_start_index:image_name_last_index]
        correct_xml_path = test_data_path + 'correct/Annotations'  + image_name + '.xml'
        print('correct_xml_path:' + correct_xml_path)

        #xmlを解析。正解座標を抽出
        # xmlファイルの読み込み
        tree = ET.parse(correct_xml_path)
        root = tree.getroot()
        correct_xmin = int(float(root[6][4][0] .text))
        correct_ymin = int(float(root[6][4][1] .text))
        correct_xmax = int(float(root[6][4][2] .text))
        correct_ymax = int(float(root[6][4][3] .text))
        #print(estimation_xmin)
        #print(type(estimation_xmin))
        
        #iou対象画像読み込み
        img = cv2.imread('../' + row[0])

        # 画像の大きさを取得
        height, width = img.shape[:2]
        print("width: " + str(width))  #256
        print("height: " + str(height)) #256

        #白色で塗りつぶす(rectangle(左上、右下))
        base = cv2.rectangle(img, (0, 0), (width, height), (255, 255,255), thickness=-1)
        base2 = base.copy()
        
        #正解データの長方形をを青色で塗りつぶす
        src1 = cv2.rectangle(base, (correct_xmin, correct_ymin), (correct_xmax, correct_ymax), (255, 255, 0), thickness=-1)
        correct_pixels = (correct_xmax - correct_xmin) * (correct_ymax - correct_ymin) 
        print('正解面積:' +  str(correct_pixels))

        #推定データの長方形を赤色で塗りつぶす
        estimation_xmin = int(float(row[3]))
        estimation_ymin = int(float(row[5]))
        estimation_xmax = int(float(row[4]))
        estimation_ymax = int(float(row[6]))
        src2 = cv2.rectangle(base2, (estimation_xmin, estimation_ymin), (estimation_xmax, estimation_ymax), (255, 0, 255), thickness=-1)
        estimation_pixels = (estimation_xmax - estimation_xmin) * (estimation_ymax - estimation_ymin) 
        print('推定面積:' +  str(estimation_pixels)) 

        #正解と推定画像合成
        dst = cv2.addWeighted(src1, 0.5, src2, 0.5, 0)
        cv2.imwrite('opencv_draw_argument.jpg', dst)

        # 重複部分抽出と面積
        ex_img = cv2.inRange(dst,LOW_COLOR,HIGH_COLOR)
        cv2.imwrite('roi.jpg', ex_img)
        white_pixels = cv2.countNonZero(ex_img)
        print('重複面積:' +  str(white_pixels))

        #iou(0.9以上を検出成功とみなすか？)
        iou = white_pixels/(correct_pixels + estimation_pixels - white_pixels)
        print('iou:' +  str(iou))
        