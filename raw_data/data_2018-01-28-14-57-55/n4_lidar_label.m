clc;
clear;

clear;

label_mat = './sync/lidar_label';
load(label_mat);

cellsize = 0.05;

pedestrian_data = gTruth.LabelData.pedestrian;
curve_data = gTruth.LabelData.curve;
lidar_data = ones(length(pedestrian_data), 9);
for i=1:length(pedestrian_data)
    pedestrian_mat = cell2mat(pedestrian_data(i));
    curve_mat = cell2mat(curve_data{i,1});
    image_px = pedestrian_mat(1) + 0.5*pedestrian_mat(3);
    image_py = pedestrian_mat(2) + 0.5*pedestrian_mat(4);
    image_cx1 = curve_mat(1,1);
    image_cy1 = curve_mat(1,2);
    image_cx2 = curve_mat(2,1);
    image_cy2 = curve_mat(2,2);
    dis_ped = cross([image_px - image_cx1, image_py - image_cy1, 0], [image_cx2 - image_cx1, image_cy2 - image_cy1, 0])/((image_cx2 - image_cx1)^2 + (image_cy2 - image_cy1)^2)^0.5;
    dis_veh = cross([1600 - image_cx1, 500 - image_cy1, 0], [image_cx2 - image_cx1, image_cy2 - image_cy1, 0])/((image_cx2 - image_cx1)^2 + (image_cy2 - image_cy1)^2)^0.5;
    dis_rel = dot([image_px - 1600, image_py - 500], [image_cx2 - image_cx1, image_cy2 - image_cy1])/((image_cx2 - image_cx1)^2 + (image_cy2 - image_cy1)^2)^0.5;
    lidar_data(i, 1) = cellsize*image_px - 80;
    lidar_data(i, 2) = -(cellsize*image_py - 25);
    lidar_data(i, 3) = cellsize*image_cx1 - 80;
    lidar_data(i, 4) = -(cellsize*image_cy1 - 25);
    lidar_data(i, 5) = cellsize*image_cx2 - 80;
    lidar_data(i, 6) = -(cellsize*image_cy2 - 25);
    lidar_data(i, 7) = cellsize*dis_ped(3);
    lidar_data(i, 8) = cellsize*dis_veh(3);
    lidar_data(i, 9) = cellsize*dis_rel;
end

savepath = './sync/lidar_data.mat';
save(savepath, 'lidar_data');
