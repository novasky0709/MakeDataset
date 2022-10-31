import sys
import os
import pathlib
import argparse
# sys.path.append(os.path.join(pathlib.Path(__file__).parent.absolute(), '.'))

class Options:
    def __init__(self):
        self.opt = None
        self.parse()
    def parse(self):
        parser = argparse.ArgumentParser(description="Argparse of  point_editor")
        parser.add_argument('--dataset_src',
                            type=str,
                            default='data_src/test',#/home/slam/devdata/pointnerf/checkpoints/scannet/scene000-T
                            help='dataset root')
        parser.add_argument('--gpu_ids',
                            type=str,
                            default='0',
                            help='gpu ids: e.g. 0  0,1,2, 0,2')
        parser.add_argument('--video_interval',
                            type=int,
                            default=10,
                            help='interval')
        parser.add_argument('--video_offset',
                            type=int,
                            default=5,
                            help='At the beginning of a video, the first few images may affect by motion-blur/exposure ...')
        parser.add_argument('--colmap_match_type', type=str,
                            default='sequential_matcher', help='type of matcher used.  Valid options: \
        					exhaustive_matcher sequential_matcher.  Other matchers not supported at this time')
        self.opt = parser.parse_args()