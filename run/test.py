import sys
import os
import pathlib
sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), '..'))
from dataloader import create_dataloader
from option import Options

if __name__ == '__main__':
    sparse = Options()
    opt = sparse.opt
    video_dataloader = create_dataloader(opt,'video')
    video_dataloader.preprocess(opt)