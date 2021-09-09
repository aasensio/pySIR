import numpy as np
import matplotlib.pyplot as pl
import pysir
import time
from tqdm import tqdm

l = [['300',-3500,10,3500]]
SIR = pysir.SIR(l)

out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
out = np.delete(out, 2, axis=1)    

stokes = SIR.synthesize(out, returnRF=False)

f, ax = pl.subplots(ncols=2, nrows=2, figsize=(16,8))
for i in range(4):
    ax.flat[i].plot(stokes[0,:], stokes[i+1,:])

# pl.tight_layout()
pl.show()