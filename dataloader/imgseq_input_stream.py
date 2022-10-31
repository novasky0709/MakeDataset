import os
class ImgSeqInputStream:
    def __init__(self,opt):
        super().__init__(opt)
    def preprocess(self,opt):
        raise NotImplementedError