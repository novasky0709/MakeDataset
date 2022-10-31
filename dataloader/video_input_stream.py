import os
import cv2
import time
from dataloader.base_input_stream import BaseInputStream
class VideoInputStream(BaseInputStream):
    def __init__(self,opt):
        super().__init__(opt)
        self.video_path  = os.path.join(self.dataset_src,'video','video.mp4')

        if not os.path.exists(self.video_path):
            print('{} is not exist, class VideoInputStream should have a "video.mp4" in dataset_src, please check it !'.format(self.video_path))
            exit(-1)
    def preprocess(self,opt):

        os.makedirs(self.img_path, exist_ok=True)
        cap = cv2.VideoCapture(self.video_path)
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))
        video_total_frame = int(cap.get(7))
        print('Preprocessing Video....   Video_fps:{}, Video_Total_Frame:{}'.format(video_fps,video_total_frame))
        interval = opt.video_interval
        offset = opt.video_offset
        save_total_num = (video_total_frame // interval) - offset
        if save_total_num <= 0:
            print('(video_total_frame // interval) - offset <0 !!! resize the video_offset or video_interval. save_total_num:{}'.format(save_total_num))
            exit(-1)
        cnt = 0
        num = 0

        t0 = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cnt += 1
                if cnt % interval == 0 and cnt >= int(offset * interval):
                    num += 1
                    # frame = cv.resize(frame, (width, height))
                    # frame = cv2.resize(frame,(640,360))
                    cv2.imwrite(self.img_path + "/%d.jpg" % (num - 1), frame)
                    remain_frame = save_total_num - num
                    t1 = time.time() - t0
                    t0 = time.time()
                    #             print("Processing %07d.jpg, remain frame: %d, remain time: %.2fs" % (num, remain_frame, remain_frame * t1))
                    print("Processing %d.jpg, remain frame: %d, remain time: %.2fs" % (
                    num - 1, remain_frame, remain_frame * t1))
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

