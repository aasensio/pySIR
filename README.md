# pySIR

Python wrapper for the Stokes Inversion based on Response functions code by Ruiz Cobo &amp; del Toro Iniesta (1992)

### Compilation
Local compilation
```python
python setup.py build_ext --inplace
```

Systemwide installation
```python
python setup.py install
```

### Example

```python
import pysir
lines = [['200,201',-500.,10.,1500.]]
SIR = pysir.SIR(lines)

psf = np.loadtxt('PSF.dat', dtype=np.float32)
SIR.setPSF(psf[:,0].flatten(), psf[:,1].flatten())
out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
stokes, rf = SIR.synthesize(out)
```

### Methods of the class

#### Instantiation
Initialize the SIR synthesis code for a set of spectral lines using

    SIR = pysir.SIR(lines)
    
The number of wavelength points to be synthesized and the number of total spectral lines in all blends can be obtained from the variables `SIR.nLambda` and `SIR.nLines`, respectively.

It only contains an input parameter `lines`, which is a list of lists containing the information for the lines to be synthesized
    Each region is defined is defined by a list containing the following elements:

    - A string defining which lines are synthesized in the region. E.g. '1,2,3'
    - Initial wavelength displacement in mA
    - Step in mA
    - Final wavelength displacement in mA

For example

    lines = [['200,201', -500.0, 10.0, 1500.0], ['2', -750.0, 10.0, 1300.0]]

#### `SIR.listLines`
Lists the lines available in SIR for synthesis


#### `SIR.setPSF(lambda, transmission)`
Define the spectral PSF to be convolved with the profiles. `lambda` is the displacement with respect to
the maximum in mA and `transmission` is the transmission of the PSF (it is normalized to unit area
in the code).
    
#### `SIR.synthesize(model, departure=None, macroturbulence=0.0, fillingFactor=1.0, stray=0.0, returnRF=True, cartesian=False)`
Carry out the synthesis and returns the Stokes parameters and the response functions to all physical variables at all depths.

##### Input parameters

###### model
The model is defined as the following array, which can be of size `[nDepth,7]`
if the electron pressure is not known and computed in hydrostatic equilibrium, or
`[nDepth,8]` if it is known.

In case the electron pressure is to be computed in hydrostatic equilibrium, the model has the following structure:

    model (float array): an array of size [nDepth, 7], where the columns contain the depth stratification of:
    
    - log tau
    - Temperature [K]    
    - Microturbulent velocity [cm/s]
    - Magnetic field strength or Bx (in cartesian) [G]
    - Line-of-sight velocity [cm/s]
    - Magnetic field inclination [deg] or By [deg] (in cartesian)
    - Magnetic field azimuth [deg] or Bz [deg] (in cartesian)

If the electron pressure is known, the model has the following structure:

    model (float array): an array of size [nDepth, 8], where the columns contain the depth stratification of:
    
    - log tau
    - Temperature [K]
    - Electron pressure [dyn cm^-2]
    - Microturbulent velocity [cm/s]
    - Magnetic field strength or Bx (in cartesian) [G]
    - Line-of-sight velocity [cm/s]
    - Magnetic field inclination [deg] or By [deg] (in cartesian) 
    - Magnetic field azimuth [deg] or Bz [deg] (in cartesian)

###### departure

An array of size `[2, nLines, nDepth]` that contains the departure coefficient (the ratio between the populations in non-LTE and in LTE) of the lower and upper levels of each transition at all heights. LTE populations are used by default if `departure` is not passed to the method.

###### macroturbulence

Macroturbulence velocity in cm/s. This velocity defines a Gaussian kernel that will convolve the final spectrum.

###### fillingFactor

Not used. Keep it at its default value.

###### stray

Not used. Keep it at its default value.

###### returnRF

If `True`, the output will contain the response functions (i.e., derivatives of the Stokes parameters with respect to the input parameters). If `False`, it only returns the synthetic spectra.

###### cartesian

If `True`, then the magnetic field is defined with the (Bx,By,Bz) components. Check the definition of the model to see which columns contain this information. If `False`, the magnetic field vector is given in spherical components (B,inclination,azimuth).
    
##### Return values

    stokes: (float array) Stokes parameters, with the first index containing the wavelength displacement and the remaining
                                containing I, Q, U and V. Size (5,nLambda)
    rf: (float array) Response functions to T, Pe, vmic, B, v, theta, phi. Size (4,nLambda,nDepth)

#### Files
The following files are needed:

    - LINEAS: defines the available lines
    - THEVENIN: defines the abundances 

#### Dependencies
    - cython
    - gfortran_linux-64
