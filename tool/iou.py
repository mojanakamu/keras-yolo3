import cv2
import numpy as np
import os
import csv
import xml.etree.ElementTree as ET
import sys

LOW_COLOR = np.array([255, 128, 128])
HIGH_COLOR = np.array([255, 128, 128])

args = sys.argv
if len(args) ==2:
    print("第1引数：" + args[1])
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_path = os.path.dirname(current_dir)
    test_data_parent_path = os.path.join(project_root_path, "data", args[1])
    print(test_data_parent_path)
    estimation_result_path = os.path.join(test_data_parent_path, "estimation")
    if os.path.exists(os.path.join(estimation_result_path, "estimation.csv")):
        print('モデル推定結果csvファイルあり')
    else:
        print('モデル推定結果csvファイルなし')
        quit()
else:
    print('以下形式でテスト対象フォルダを指定してください')
    print('$ python iou.py  <folder> ')
    quit()
    
test_data_img_path = os.path.join(test_data_parent_path, "img")
correct_pixels_path = os.path.join(test_data_img_path, "correct_pixels")
estimation_pixels_path = os.path.join(test_data_img_path, "estimation_pixels")
roi_path = os.path.join(test_data_img_path, "roi")

data=[
        ("img_path", 'predicted_class', 'score', 'estimation_pixels', 'correct_pixels', 'roi'),
]

#正解、推定領域の画像保存先ディレクトリ作成
os.makedirs(correct_pixels_path, exist_ok=True)
os.makedirs(estimation_pixels_path, exist_ok=True)
os.makedirs(roi_path, exist_ok=True)

with open(os.path.join(estimation_result_path, "estimation.csv"), 'r') as f:
    reader = csv.reader(f)
    header = next(reader) 

    for i,row in enumerate(reader):
        print('{0}:{1}'.format(i, row))

        #画像パス名から正解データのxmlパスを特定
        print('image_path:' + row[0])
        image_name_start_index = row[0].rfind('/')
        image_name_last_index = row[0].rfind('.')
        image_name =row[0][image_name_start_index+1:image_name_last_index]
        print(image_name)
        #correct_xml_path = test_data_path + 'correct/Annotations'  + image_name + '.xml'
        correct_xml_path = os.path.join(test_data_parent_path, "correct", "Annotations", image_name + ".xml")
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
        img = cv2.imread(row[0])

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
        correct_rec = cv2.addWeighted(src1, 0.5, cv2.imread(row[0]), 0.5, 0)
        cv2.imwrite(os.path.join(correct_pixels_path, image_name + ".jpg"), correct_rec)
        print('正解面積:' +  str(correct_pixels))

        #推定データの長方形を赤色で塗りつぶす
        estimation_xmin = int(float(row[3]))
        estimation_ymin = int(float(row[5]))
        estimation_xmax = int(float(row[4]))
        estimation_ymax = int(float(row[6]))
        src2 = cv2.rectangle(base2, (estimation_xmin, estimation_ymin), (estimation_xmax, estimation_ymax), (255, 0, 255), thickness=-1)
        estimation_pixels = (estimation_xmax - estimation_xmin) * (estimation_ymax - estimation_ymin) 
        estimation_rec = cv2.addWeighted(src2, 0.5, cv2.imread(row[0]), 0.5, 0)
        cv2.imwrite(os.path.join(estimation_pixels_path, image_name + ".jpg"), estimation_rec)
        print('推定面積:' +  str(estimation_pixels)) 

        #正解と推定画像合成
        dst = cv2.addWeighted(src1, 0.5, src2, 0.5, 0)
        dst_rec = cv2.addWeighted(dst, 0.5, cv2.imread(row[0]), 0.5, 0)
        cv2.imwrite(os.path.join(roi_path, image_name + ".jpg"), dst_rec)

        # 重複部分抽出と面積
        ex_img = cv2.inRange(dst,LOW_COLOR,HIGH_COLOR)
        cv2.imwrite('roi.jpg', ex_img)
        white_pixels = cv2.countNonZero(ex_img)
        print('重複面積:' +  str(white_pixels))

        #iou(0.9以上を検出成功とみなすか？)
        iou = white_pixels/(correct_pixels + estimation_pixels - white_pixels)
        print('iou:' +  str(iou))

        data.append((row[0], row[1], row[2], os.path.join(estimation_pixels_path, image_name + ".jpg"), os.path.join(correct_pixels_path, image_name + ".jpg"), os.path.join(roi_path, image_name + ".jpg")))
    
    with open(os.path.join(estimation_result_path, "comparison.csv"), 'w') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row) 

    
        