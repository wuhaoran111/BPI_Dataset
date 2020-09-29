clear;
clc;

pc_listfile = fopen('./sync/sync_pcl1_list.txt', 'r');
while feof(pc_listfile) ~=1
    pc_list = fgetl(pc_listfile);
    timestamp = pc_list(13:31);
    savepath = ['./sync_pcl1_mat/' timestamp];
    pc = pcread(pc_list);
    pc_location = pc.Location;
    save(savepath, 'pc_location')
end
