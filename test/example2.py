import numpy as np
import matplotlib.pyplot as pl
import pysir
import time
from tqdm import tqdm

l = [['1',-500,10,1500]]
SIR = pysir.SIR(l)

psf = np.loadtxt('PSF.dat', dtype=np.float32)
SIR.set_PSF(psf[:,0].flatten(), psf[:,1].flatten())
out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
out = np.delete(out, 2, axis=1)    

start = time.time()        
            
for i in tqdm(range(50)):
    stokes = SIR.synthesize(out, returnRF=True)

print('Elapsed time 50 synthesis : {0} s'.format(time.time()-start))

start = time.time()        
for i in tqdm(range(50)):
    stokes = SIR.synthesize(out, returnRF=False)

print('Elapsed time 50 synthesis : {0} s'.format(time.time()-start))
