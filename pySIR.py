from __future__ import print_function
import numpy as np
import sir
import matplotlib.pyplot as pl
from ipdb import set_trace as stop

__all__ = ["listLinesSIR", "initializeSIR", "synthesizeSIR"]

def listLinesSIR():
    """List the lines available in SIR for synthesis
        
    """
    f = open('LINEAS', 'r')
    lines = f.readlines()
    f.close()

    print("Available lines:")
    for l in lines[:-1]:
        print(l[:-1])

def initializeSIR(lines):
    """Initialize the SIR synthesis code for a set of spectral lines
    
    Args:
        lines (list): list of lists containing the information for the lines to be synthesized
                    Each region is defined is defined by a list containing the following elements:
                     - A string defining which lines are synthesized in the region. E.g. '1,2,3'
                     - Initial wavelength displacement in mA
                     - Step in mA
                     - Final wavelength displacement in mA

                     E.g. lines = [['1', -500.0, 10.0, 1500.0], ['2', -750.0, 10.0, 1300.0]]
    
    Returns:
        int: the number of wavelength points to be synthesized

    """
    f = open('malla.grid', 'w')
    f.write("IMPORTANT: a) All items must be separated by commas.                 \n")
    f.write("           b) The first six characters of the last line                \n")
    f.write("          in the header (if any) must contain the symbol ---       \n")
    f.write("\n")                                                                       
    f.write("Line and blends indices   :   Initial lambda     Step     Final lambda \n")
    f.write("(in this order)                    (mA)          (mA)         (mA)     \n")
    f.write("-----------------------------------------------------------------------\n")

    for i in range(len(lines)):
        f.write("{0}    :  {1}, {2}, {3}".format(lines[i][0], lines[i][1], lines[i][2], lines[i][3]))
    f.close()
        
    return sir.init()

def setPSF(xPSF, yPSF):
    """Define the spectral PSF to be convolved with the profiles
    
    Args:
        xPSF (float): wavelength with respect to the maximum (in mA) [nLambda]
        yPSF (float): transmission for each wavelength displacement. It is not necessary to normalize it to unit area [nLambda]    
    """
    sir.setPSF(xPSF, yPSF)

def synthesizeSIR(model, macroturbulence=0.0, fillingFactor=1.0, stray=0.0, returnRF=True):
    """Carry out the synthesis and returns the Stokes parameters and the response 
    functions to all physical variables at all depths
    
    Args:
        model (float array): an array of size [nDepth x 7] or [nDepth x 8], where the columns contain the depth stratification of:
            - log tau
            - Temperature [K]
            - Electron pressure [dyn cm^-2]  (optional)
            - Microturbulent velocity [km/s]
            - Magnetic field strength [G]
            - Line-of-sight velocity [km/s]
            - Magnetic field inclination [deg]
            - Magnetic field azimuth [deg]
        macroturbulence (float, optional): macroturbulence velocity [km/s]. Default: 0
        fillingFactor (float, optional): filling factor. Default: 1
        stray (float, optional): stray light in %. Default: 0
        returnRF (bool, optional): return response functions
    
    Returns:
        stokes: (float array) Stokes parameters, with the first index containing the wavelength displacement and the remaining
                                containing I, Q, U and V. Size (5,nLambda)
        rf: (float array) Response functions to T, Pe, vmic, B, v, theta, phi, all of size (4,nLambda,nDepth), plus the RF to macroturbulence of size (4,nLambda)
                        It is not returned if returnRF=False
    """
    if (model.shape[1] == 7):
        model = np.insert(model, 2, -np.ones(model.shape[0]), axis=1)
# Boundary condition for Pe
        model[-1,2] = 1.11634e-01        

    if (returnRF):
        stokes, rf = sir.synthRF(model, macroturbulence, fillingFactor, stray)
        return stokes, rf
    else:
        stokes = sir.synth(model, macroturbulence, fillingFactor, stray)        
        return stokes    
    return stokes, rf

if (__name__ == "__main__"):
    listLinesSIR()
    l = [['1',-500.,10.,1500.]]
    nLambda = initializeSIR(l)
    psf = np.loadtxt('PSF.dat', dtype=np.float32)
    setPSF(psf[:,0].flatten(), psf[:,1].flatten())
    out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
    out = np.delete(out, 2, axis=1)    
    stokes, rf = synthesizeSIR(out)

    f, ax = pl.subplots(ncols=4, nrows=2, figsize=(16,6))
    for i in range(4):
        ax[0,i].plot(stokes[0,:], stokes[i+1,:])
        ax[1,i].imshow(rf[0][i,:,:].T)

    pl.tight_layout()
