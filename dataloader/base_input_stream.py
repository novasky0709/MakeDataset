import os
class BaseInputStream:
    def __init__(self,opt):
        self.dataset_src = os.path.join(os.getcwd(),'..',opt.dataset_src)
        self.img_path = os.path.join(self.dataset_src,'images')
        self.dataset_dst_path = os.path.join(self.dataset_src,'result_des')
        self.colmap_project_path = os.path.join(self.dataset_src, 'colmap_result')
        os.makedirs(self.dataset_dst_path, exist_ok=True)
        os.makedirs(os.path.join(self.dataset_dst_path,'color'), exist_ok=True)
        os.makedirs(os.path.join(self.dataset_dst_path, 'depth'), exist_ok=True)
        os.makedirs(os.path.join(self.dataset_dst_path, 'intrinsic'), exist_ok=True)
        os.makedirs(os.path.join(self.dataset_dst_path, 'pose'), exist_ok=True)
        os.makedirs(self.colmap_project_path, exist_ok=True)
        self.dataset_dst_img_path = os.path.join(self.dataset_dst_path,'images')
        self.dataset_dst_pose_path = os.path.join(self.dataset_dst_path,'pose')
        if not os.path.isdir(self.dataset_src):
            print('{} is not a dir, please check it !'.format(self.dataset_src))
            exit(-1)
    def preprocess(self,opt):
        raise NotImplementedError