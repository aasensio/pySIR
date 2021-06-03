import numpy as np
import matplotlib.pyplot as pl
import pysir
import time

pysir.list_lines()
l = [['1',-500,10,1500]]
nLambda = pysir.initialize(l)
psf = np.loadtxt('PSF.dat', dtype=np.float32)
pysir.set_PSF(psf[:,0].flatten(), psf[:,1].flatten())
out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
out = np.delete(out, 2, axis=1)    

start = time.time()        
            
for i in range(50):
    stokes = pysir.synthesize(out, returnRF=True)

print('Elapsed time 50 synthesis : {0} s'.format(time.time()-start))

start = time.time()        
for i in range(50):
    stokes = pysir.synthesize(out, returnRF=False)

print('Elapsed time 50 synthesis : {0} s'.format(time.time()-start))
