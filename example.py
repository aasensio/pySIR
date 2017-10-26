import numpy as np
import matplotlib.pyplot as pl
import pysir

pysir.list_lines()
l = [['1',-500.,10.,1500.]]
nLambda = pysir.initialize(l)
psf = np.loadtxt('PSF.dat', dtype=np.float32)
pysir.set_PSF(psf[:,0].flatten(), psf[:,1].flatten())
out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
out = np.delete(out, 2, axis=1)    
stokes, rf = pysir.synthesize(out)

f, ax = pl.subplots(ncols=4, nrows=2, figsize=(16,6))
for i in range(4):
    ax[0,i].plot(stokes[0,:], stokes[i+1,:])
    ax[1,i].imshow(rf[0][i,:,:].T)

pl.tight_layout()
pl.show()