from __future__ import division  # floating point division
import csv
import random
import math
import numpy as np

import dataloader as dtl
import regressionalgorithms as algs
import plotfcns

def l2err(prediction,ytest):
    """ l2 error (i.e., root-mean-squared-error) """
    return np.linalg.norm(np.subtract(prediction,ytest))





if __name__ == '__main__':

    
    trainsize = 7000
    testsize = 3000
    numparams = 1
    numruns = 1
    
    regressionalgs = {
                'FSLinearRegression5': algs.FSLinearRegression({'features': range(150)}),
                'FSLinearRegression50': algs.FSLinearRegression({'features': range(384)}),
             }       
    numalgs = len(regressionalgs)

    errors = {}
    for learnername in regressionalgs:
        errors[learnername] = np.zeros((numparams,numruns))
        
    trainset, testset = dtl.load_ctscan(trainsize,testsize)
    print('Running on train={0} and test={1}').format(trainset[0].shape[0], testset[0].shape[0])

    # Currently only using 1 parameter setting (the default) and 1 run
    p = 0
    r = 0
    params = {}
    import time
    for learnername, learner in regressionalgs.iteritems():
        learner.reset(params)
        print 'Running learner = ' + learnername + ' on parameters ' + str(learner.getparams())
		start=time.time()
        L2_penalty = 0.01 #manually change the penalty term here 
        weights = learner.learn_ridge(trainset[0], trainset[1], L2_penalty)
        predictions = learner.predict(testset[0])
        rrerr = geterror(testset[1], predictions)
		stop=time.time()
		print 'for Ridge regression with L2_penalty of' +str(L2_penalty)+' the error is' +str(rrerr)
		print 'time taken ',stop-start
      


                
                

