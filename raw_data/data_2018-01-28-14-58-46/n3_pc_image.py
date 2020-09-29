"""
this file saves images of pc
"""

import os
import scipy.io as scio
import numpy as np
import cv2

def pc_mat2image(pc_mat):
    x_min = -80
    x_max = 120
    y_min = -25
    y_max = 25
    cell_size = 0.05
    row = int((y_max - y_min)/cell_size)
    col = int((x_max - x_min)/cell_size)
    image = np.zeros((row, col, 3), dtype=np.uint8)

    pc_data = scio.loadmat('./sync_pcl1_mat/'+pc_mat)['pc_location']

    for i in range(pc_data.shape[0]):
        x = pc_data[i, 0] - x_min
        y = pc_data[i, 1] - y_min
        x_image = int(x/cell_size)
        y_image = row - int(y/cell_size)
        if x_image >= 0 and x_image < col and y_image >= 0 and y_image < row:
            image[y_image, x_image, 2] = 255
    cv2.imwrite('./sync_pcl1_image/' + pc_mat[0:19] +'.png', image)


if not os.path.exists('./sync_pcl1_image'):
    os.makedirs('./sync_pcl1_image')

for pc_mat in os.listdir('./sync_pcl1_mat'):

    pc_mat2image(pc_mat)

print('finish')