"""
this file is to add keypoints and orientation to csv file
"""

import csv

sync_data_file = './sync/sync_data.csv'
image_kp_file = './sync/image_kp.txt'
image_orientation_file = './sync/image_orientation.txt'

with open(sync_data_file) as sync_data:
    sync_data_reader = csv.reader(sync_data)
    sync_data_list = list(sync_data_reader)

with open(image_kp_file) as image_kp:
    image_kp_list = image_kp.readlines()

with open(image_orientation_file) as image_orientation:
    image_orientation_list = image_orientation.readlines()

kp_title_list = ['01-mouth', '02-neck', '03-l_shoulder', '04-l_elbow', '05-l_wrist', '06-r_shoulder', '07-r_elbow',
                 '08-r_wrist', '09-l_hip', '10-l_knee', '11-l_ankle', '12-r_hip', '13-r_knee', '14-r_ankle', '15-l_eye',
                 '16-r_eye', '17-l_ear', '18-r_ear']
ori_title_list = ['46-orientation']

sync_data_final = [sync_data_list[0] + kp_title_list + ori_title_list]
for i in range(1,len(sync_data_list)):
    image_kp_num_list = []
    for j in range(18):
        image_kp_num_list.append(image_kp_list[i-1][3*j:3*j+2])
    image_ori_num_list = []
    if image_orientation_list[i-1][0] == 'U':
        image_ori_num_list.append('-1')
    else:
        image_ori_num_list.append(image_orientation_list[i-1][0:-2])
    sync_data_final.append(sync_data_list[i] + image_kp_num_list +image_ori_num_list)

with open('./sync/sync_data_final.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(sync_data_final)

print('finish')