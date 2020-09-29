"""
this file fuse data from different sources
"""

import os
import shutil
import numpy as np
import csv
import scipy.io as scio

can_filename = './can/can.csv'
meobj_filename = './me/ivsensormeobj.csv'
meroad_filename = './me/ivsensormeroad.csv'
imu_filename = './imu/imudata.csv'

# time stamp list of all sensors
lidar_label_data = scio.loadmat('./sync/lidar_data.mat')['lidar_data']

with open(can_filename) as can:
    can_reader = csv.reader(can)
    can_list = list(can_reader)
    can_time_list = []
    can_sync_list = []
    for i in range(1, len(can_list)):
        can_time_list.append(int(can_list[i][0]))
        can_sync_list.append(can_list[i][1])
    can_time = np.array(can_time_list) * 1e-9

with open(meobj_filename) as meobj:
    meobj_reader = csv.reader(meobj)
    meobj_list = list(meobj_reader)
    meobj_time_list = []
    meobj_sync_list = []
    for i in range(1, len(meobj_list)):
        meobj_time_list.append(int(meobj_list[i][0]))
        # me_sync_list.append(me_list[i][1:5]+me_list[i][8:10])
        meobj_sync_list.append(meobj_list[i][1:-1])
    meobj_time = np.array(meobj_time_list) * 1e-9

with open(meroad_filename) as meroad:
    meroad_reader = csv.reader(meroad)
    meroad_list = list(meroad_reader)
    meroad_time_list = []
    meroad_sync_list = []
    for i in range(1, len(meroad_list)):
        meroad_time_list.append(int(meroad_list[i][0]))
        # me_sync_list.append(me_list[i][1:5]+me_list[i][8:10])
        meroad_sync_list.append(meroad_list[i][1:3]+meroad_list[i][7:9])
    meroad_time = np.array(meroad_time_list) * 1e-9

with open(imu_filename) as imu:
    imu_reader = csv.reader(imu)
    imu_list = list(imu_reader)
    imu_time_list = []
    imu_sync_list = []
    for i in range(1, len(imu_list)):
        imu_time_list.append(int(imu_list[i][0]))
        imu_sync_list.append(imu_list[i][29])
    imu_time = np.array(imu_time_list) * 1e-9

image_list = []
for image_file in os.listdir('./image'):
    image_list.append(image_file[0:19])
image_list = sorted(image_list)
image_time_list = map(lambda x: int(x), image_list)
image_time = np.array(image_time_list) * 1e-9

pc_image_list = []
for pc_image_file in os.listdir('./sync_pcl1_image'):
    pc_image_list.append(pc_image_file[0:19])
pc_image_list = sorted(pc_image_list)
pc_image_time_list = map(lambda x: int(x), pc_image_list)
pc_image_time = np.array(pc_image_time_list) * 1e-9


# sync list based on pc_image
sync_list = []
for i in range(len(pc_image_time_list)):
    time = pc_image_time[i]
    rel_time = time - pc_image_time[0]
    dev_can = abs(can_time - time)
    num_can = dev_can.argmin()
    dev_meobj = abs(meobj_time - time)
    num_meobj = dev_meobj.argmin()
    dev_meroad = abs(meroad_time - time)
    num_meroad = dev_meroad.argmin()
    dev_imu = abs(imu_time - time)
    num_imu = dev_imu.argmin()
    dev_image = abs(image_time - time)
    num_image = dev_image.argmin()
    sync_list.append([rel_time, i, time, num_can, can_time_list[num_can], num_meobj, meobj_time_list[num_meobj], num_meroad, meroad_time_list[num_meobj], num_meobj, meobj_time_list[num_meobj], num_imu, imu_time_list[num_imu], num_image, image_time_list[num_image]])

with open('./sync/sync_list.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerows(sync_list)

# synchronized data by sync data
"""
for each element of the list
1-number_lidar 2-rel_time_lidar time_lidar 3-vehicle_speed_can 4-obj_id_me 5-obj_x_me 6-obj_y_me 7-obj_relspeed_me 8-class_me 9-acc_imu
"""


sync_data = [['0-number', '1-lidar_rel_time', '2-lidar_time', '3-can_veh_speed', '4-imu_veh_acc', '5-meroad_ltype',
              '6-meroad_rtype', '7-meroad_loffset', '8-meroad-roffset', '9-lidar_ped_x', '10-lidar_ped_y',
              '11-lidar_curve_x1', '12-lidar_curve_y1', '13-lidar_curve_x2', '14-lidar_curve_y2', '15-lidar_pc_lat',
              '16-lidar_vc_lat', '17-lidar_pv_lon', '18-me_is_valid', '19-me_obj_id', '20-me_obj_x', '21-me_obj_y', '22-me_obj_relspeed',
              '23-me_obj_width', '24-me_obj_length', '25-me_obj_height', '26-me_obj_speed', '27-me_obj_class']]
for element in sync_list:
    sync_data.append([element[1], element[0], element[2], can_sync_list[element[3]], imu_sync_list[element[9]]] +
                     meroad_sync_list[element[7]] + list(lidar_label_data[element[1]]) + [1] + meobj_sync_list[element[5]])

with open('./sync/sync_data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(sync_data)
with open('./sync/sync_data_ori.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(sync_data)
print('finish')


