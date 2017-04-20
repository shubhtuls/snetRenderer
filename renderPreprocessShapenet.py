import os
import os.path as osp

from renderer.BlenderRenderer import Renderer

import numpy as np
import copy
import startup
from Pose import Pose
import ast
import numpy as np
import scipy.io as sio
import skimage.io
import math

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

import cPickle as pickle
import errno

class shapenetRenderer():
    def __init__(self, numPoses=10, useV1=True, minPose=[-180,0,0], maxPose=[180,40,1]):
        self.numPoses = numPoses

        self.useV1 = useV1
        self._initModelInfo()
        self.minPose = minPose
        self.maxPose = maxPose

        #print self.synsetModels[0][0]
        #self.renderer = Renderer([self.synsetModels[0][0]],self.imX, self.imY)
        self.renderer = Renderer([self.synsetModels[0][0]])

    def renderAllSynsets(self, minS=0, maxS=None):
        if(maxS == None):
            maxS = len(synsets)
            
        for sId in range(minS, maxS):
            synset = self.synsets[sId]
            print synset
            for mId in range(len(self.synsetModels[sId])):
            #for mId in range(2):
                print mId
                mName = self._loadNewModel(sId, mId)
                renderDir = osp.join(self.config['renderPrecomputeDir'], synset, mName)
                mkdir_p(renderDir)
                poseSamples = self._randomPoseSamples()

                infoFile = osp.join(renderDir,'poseInfo.pickle')
                with open(infoFile, 'w') as f:
                    pickle.dump([poseSamples], f)
                #self._saveModelRenderings(renderDir, poseSamples)
                self.renderer.renderViews(poseSamples, renderDir)

    def _loadNewModel(self, synsetId, modelId):
        mPath = self.synsetModels[synsetId][modelId]
        if(self.useV1):
            mName = (mPath.split('/'))[-2]
        else:
            mName = (mPath.split('/'))[-3]
        self.renderer.reInit([mPath])
        return mName

    def _randomPoseSamples(self):
        poseSamples = []
        for n in range(self.numPoses):
            poseSample = [np.random.randint(self.minPose[ix], self.maxPose[ix]) for ix in range(3)]
            poseSamples.append(Pose({'rot':poseSample}))
        return poseSamples

    def _initModelInfo(self):
        self.config = startup.params()
        #self.synsets = ['02834778','02858304','02924116','03790512','04256520','04468005','03211117']
        if(self.useV1):
            self.synsets = [f[0:-4] for f in os.listdir(self.config['shapenetDir']) if f.endswith('.csv')]
            self.synsets.sort()
            self.synsetModels = [[osp.join(self.config['shapenetDir'],s,f,'model.obj') for f in os.listdir(osp.join(self.config['shapenetDir'],s)) if len(f) > 3] for s in self.synsets]
        else:
            self.synsets = [f for f in os.listdir(self.config['shapenetDir']) if len(f)>3]
            self.synsets.sort()
            self.synsetModels = [[osp.join(self.config['shapenetDir'],s,f,'models','model_normalized.obj') for f in os.listdir(osp.join(self.config['shapenetDir'],s)) if len(f) > 3] for s in self.synsets]
            
