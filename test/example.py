import numpy as np
import matplotlib.pyplot as pl
import pysir
import time
from tqdm import tqdm

l = [['200,201',-500,10,1500]]
SIR = pysir.SIR(l)

psf = np.loadtxt('PSF.dat', dtype=np.float32)
SIR.set_PSF(psf[:,0].flatten(), psf[:,1].flatten())
out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
out = np.delete(out, 2, axis=1)    

departure = np.ones((2, SIR.nLines, out.shape[0]), dtype=np.float32)

stokes, rf = SIR.synthesize(out, departure=departure)

nz = out.shape[0]
rf_numerical = np.zeros((4, SIR.nLambda, nz))
for i in tqdm(range(73)):
    out_new = np.copy(out)
    out_new[i,1] += 1.0
    stokes_new = SIR.synthesize(out_new, departure=departure, returnRF=False)
    rf_numerical[:,:,i] = (stokes_new[1:,:] - stokes[1:,:]) / 1.0

f, ax = pl.subplots(ncols=4, nrows=3, figsize=(16,8))
for i in range(4):
    ax[0,i].plot(stokes[0,:], stokes[i+1,:])
    im = ax[1,i].imshow(rf[0][i,:,:].T)
    pl.colorbar(im, ax=ax[1,i])
    im = ax[2,i].imshow(rf_numerical[i,:,:].T)
    pl.colorbar(im, ax=ax[2,i])

# pl.tight_layout()
pl.show()

# start = time.time()        
            
# for i in range(50):
#     stokes, rf = pysir.synthesize(out, returnRF=True)

# print('Elapsed time 50 synthesis : {0} s'.format(time.time()-start))
