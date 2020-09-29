import os
import shutil
import numpy as np


image_list = []
for image_file in os.listdir('./image'):
    image_list.append(image_file[0:19])
image_list = sorted(image_list)
image_time_list = map(lambda x: int(x), image_list)
image_time = np.array(image_time_list) * 1e-9

pc_list = []
for pc_file in os.listdir('./pcl1'):
    pc_list.append(pc_file[0:10] + pc_file[11:20])
pc_list = sorted(pc_list)
pc_time_list = map(lambda x: int(x), pc_list)
pc_time = np.array(pc_time_list) * 1e-9

sync_list = []
for i in range(len(pc_time_list)):
    time = pc_time[i]
    dev_image = abs(image_time - time)
    num_image = dev_image.argmin()
    sync_list.append([i, pc_time_list[i], num_image, image_time_list[num_image]])

if not os.path.exists('./sync_image'):
    os.makedirs('./sync_image')

for element in sync_list:
    image_name_old = str(element[3]) + '.png'
    image_name_new = str(element[1]) + '.png'
    shutil.copyfile('./image/'+image_name_old, './sync_image/'+image_name_new)

print('finish')
