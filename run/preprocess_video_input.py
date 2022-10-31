import sys
import os
import pathlib
import pandas as pd
import torch
import codecs
import shutil
import numpy as np
sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), '..'))
sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), '..','LLFF'))
from dataloader import create_dataloader
from option import Options
from LLFF.llff.poses.pose_utils import gen_poses
from utils.read_write_model import read_images_binary,read_cameras_binary,read_points3D_binary,write_images_text,write_cameras_text,write_points3D_text
from utils.util import q2homoRot,q2rot
if __name__ == '__main__':
    sparse = Options()
    opt = sparse.opt
    video_dataloader = create_dataloader(opt,'video')
    if not os.path.exists(video_dataloader.img_path):
        video_dataloader.preprocess(opt)
        exit(0)
    print("Preprocess Done")
    # if opt.colmap_match_type != 'exhaustive_matcher' and opt.colmap_match_type != 'sequential_matcher':
    #     print('ERROR: matcher type ' + opt.colmap_match_type + ' is not valid.  Aborting')
    #     sys.exit()
    # gen_poses(video_dataloader.dataset_src,opt.colmap_match_type) # generate pose,refer to LLFF cam2pos
    # convert bin2text





    colmap_imgs_bin_path = os.path.join(video_dataloader.dataset_src,'colmap_result', 'dense','sparse', 'images.bin')
    colmap_cams_bin_path = os.path.join(video_dataloader.dataset_src, 'colmap_result', 'dense','sparse',  'cameras.bin')
    colmap_ptrs_bin_path = os.path.join(video_dataloader.dataset_src, 'colmap_result', 'dense','sparse', 'points3D.bin')
    write_images_text(read_images_binary(colmap_imgs_bin_path),os.path.join(video_dataloader.dataset_src,'colmap_result', 'dense','sparse', 'images.txt'))
    write_cameras_text(read_cameras_binary(colmap_cams_bin_path),os.path.join(video_dataloader.dataset_src, 'colmap_result', 'dense','sparse', 'cameras.txt'))
    write_points3D_text(read_points3D_binary(colmap_ptrs_bin_path),os.path.join(video_dataloader.dataset_src, 'colmap_result', 'dense','sparse', 'points3D.txt'))
    # # copy imgs
    imgList = os.listdir(os.path.join(video_dataloader.dataset_src,'colmap_result','dense','images'))
    cnt = 0
    # print('Copying imgs...')
    # for img in imgList:
    #     newName = str(str(cnt)+'.jpg')
    #     cnt += 1
    #     src = os.path.join(video_dataloader.img_path,img)
    #     dst = os.path.join(video_dataloader.dataset_dst_path,'color',newName)
    #     shutil.copyfile(src, dst)
    # print('Copy down...')
    # copy camera pose
    colmap_pose_table_path = os.path.join(video_dataloader.dataset_src,'colmap_result', 'dense','sparse', 'images.txt')
    print(colmap_pose_table_path)
    pose_table = pd.read_table(colmap_pose_table_path)
    rawDf = []
    nameList = []
    Df = []
    qMat = []
    for i in range(len(imgList)):
        print(i,len(imgList))
        print(pose_table.loc[i * 2 + 3].values[0])
        line = pose_table.loc[i * 2 + 3].values[0]
        rawDf.append(line)
    print(rawDf)
    postList = []  # 存有每个图片的位姿信息
    xList = []
    yList = []
    zList = []

    for i in rawDf:
        line = i.split(' ')
        Df.append(line)
        nameList.append(line[-1])

        qMat = []
        qTrans = []
        for i in line[1:5]:
            qMat.append(float(i))
        for i in line[5:8]:
            qTrans.append(float(i))

        w2per = q2homoRot(qMat, qTrans)
        # 转置 计算成相机到世界的

        testMat = torch.tensor(w2per)

        tra = testMat[:3, :3]
        pos = testMat[:3, 3].reshape(3, 1)

        invMat = torch.transpose(tra, 0, 1)
        #     print((-1*invMat).shape)
        #     print((-1*invMat))

        #     print(pos.shape)
        #     print(pos)

        # # 左手席右手系转换
        #     le2ri = torch.tensor([[1,0,0],[0,1,0],[0,0,-1]])
        #     invMat = torch.mm(le2ri.to(torch.float64),invMat)

        finalPos = torch.mm((-1 * invMat), pos.to(torch.float64))
        print("finalpos", finalPos)

        tem = torch.cat((invMat, finalPos), 1)
        finalMat = torch.cat((tem, torch.tensor([[0, 0, 0, 1]])), 0)
        #     print(finalMat)
        postList.append(finalMat)

    os.makedirs(video_dataloader.dataset_dst_pose_path, exist_ok=True)
    for ind in range(len(postList)):
        txtName = nameList[ind].split('.')[0] + ".txt"
        print(txtName)
        with codecs.open(os.path.join(video_dataloader.dataset_dst_pose_path, txtName), 'w', 'gb18030') as f:
            temList = postList[ind].tolist()
            xList.append(temList[0][-1])
            yList.append(temList[1][-1])
            zList.append(temList[2][-1])
            for item in temList:
                #             print(item)
                temLine = ' '.join(str(i) for i in item)
                temLine = temLine + "\n"
                f.write(temLine)
        imgName = nameList[ind].split('.')[0] + ".jpg"
        src = os.path.join(video_dataloader.img_path,imgName)
        dst = os.path.join(video_dataloader.dataset_dst_path,'color',imgName)
        shutil.copyfile(src, dst)
    bbox = [min(xList), min(yList), min(zList), max(xList), max(yList), max(zList)]
    np.savetxt(os.path.join(video_dataloader.dataset_dst_path,'bbox.txt'),bbox)
    print(bbox)