import os
import os.path as osp
import sys
import platform

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
        print 'added {}'.format(path)

add_path(os.getcwd())

def params():
    config = {}
    config['basedir'] = os.getcwd()
    config['shapenetDir'] = '/data1/shubhtuls/cachedir/Datasets/shapeNetCoreV1/' # shapenet folder, not used in this code
    #config['shapenetDir'] = '/data0/shubhtuls/datasets/ShapeNetCore.v2/' # shapenet folder, not used in this code
    config['renderPrecomputeDir'] = osp.join('/data0/shubhtuls/code/snetRenderer','cachedir','blenderRenderPreprocess')
    return config