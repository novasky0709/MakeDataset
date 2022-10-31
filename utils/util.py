import numpy as np
def q2rot(qMat):
    # qMat格式  qw qx qy qz
    w = qMat[0]
    x = qMat[1]
    y = qMat[2]
    z = qMat[3]
    #     rotMat = [[1-2*y**2-2*z**2,2*x*y+2*w*z,2*x*z-2*w*y],
    #               [2*x*y-2*w*z,1-2*x**2-2*z**2,2*y*z+2*w*x],
    #               [2*x*z+2*w*y,2*y*z-2*w*x+1-2*x**2-2*y**2]]

    rotMat = np.mat([[1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y - 2 * w * z, 2 * x * z + 2 * w * y],
                     [2 * x * y + 2 * w * z, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z - 2 * w * x],
                     [2 * x * z - 2 * w * y, 2 * y * z + 2 * w * x, 1 - 2 * x ** 2 - 2 * y ** 2]])
    return rotMat


"""通过四元数，平移矩阵获得奇次矩阵"""


def q2homoRot(qMat, qTrans):
    # qMat格式  qw qx qy qz
    # qTrans格式 x y z
    qw = qMat[0]
    qx = qMat[1]
    qy = qMat[2]
    qz = qMat[3]
    x = qTrans[0]
    y = qTrans[1]
    z = qTrans[2]

    #     rotMat = [[1-2*y**2-2*z**2,2*x*y+2*w*z,2*x*z-2*w*y],
    #               [2*x*y-2*w*z,1-2*x**2-2*z**2,2*y*z+2*w*x],
    #               [2*x*z+2*w*y,2*y*z-2*w*x+1-2*x**2-2*y**2]]

    rotMat = np.mat([
        [1 - 2 * qy ** 2 - 2 * qz ** 2, 2 * qx * qy - 2 * qw * qz, 2 * qx * qz + 2 * qw * qy, x],
        [2 * qx * qy + 2 * qw * qz, 1 - 2 * qx ** 2 - 2 * qz ** 2, 2 * qy * qz - 2 * qw * qx, y],
        [2 * qx * qz - 2 * qw * qy, 2 * qy * qz + 2 * qw * qx, 1 - 2 * qx ** 2 - 2 * qy ** 2, z],
        [0, 0, 0, 1]
    ])
    return rotMat
