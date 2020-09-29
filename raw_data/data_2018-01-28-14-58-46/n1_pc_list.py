"""
this file is to generate list of filenames of pc
"""
import os
import shutil


if not os.path.exists('./sync_pcl1'):
    os.makedirs('./sync_pcl1')

filename_list = []

for imagename in os.listdir('./sync_image'):
    pc_name_old = imagename[0:10] + '.' + imagename[10:19] + '.pcd'
    pc_name_new = imagename[0:19] + '.pcd'
    shutil.copyfile('./pcl1/'+pc_name_old, './sync_pcl1/'+pc_name_new)

for filename in os.listdir('./sync_pcl1'):
    if len(filename_list) < 0.5:
        filename_list.append('./sync_pcl1/' + filename)
    else:
        filename_list.append('\n' + './sync_pcl1/' + filename)

if not os.path.exists('./sync'):
    os.makedirs('./sync')

pc_list = open('./sync/sync_pcl1_list.txt', 'w')
pc_list.writelines(filename_list)
pc_list.close()

if not os.path.exists('./sync_pcl1_mat'):
    os.makedirs('./sync_pcl1_mat')
print('process ends')
