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
pysir.listLines()
lines = [['1',-500.,10.,1500.]]
nLambda = pysir.initialize(lines)
psf = np.loadtxt('PSF.dat', dtype=np.float32)
setPSF(psf[:,0].flatten(), psf[:,1].flatten())
out = np.loadtxt('model.mod', dtype=np.float32, skiprows=1)[:,0:8]
stokes, rf = pysir.synthesize(out)
```

#### listLines
Lists the lines available in SIR for synthesis

#### initialize(lines)
Initialize the SIR synthesis code for a set of spectral lines. It outputs the number of wavelength points to be synthesized.
    
lines: list of lists containing the information for the lines to be synthesized
    Each region is defined is defined by a list containing the following elements:

    - A string defining which lines are synthesized in the region. E.g. '1,2,3'
    - Initial wavelength displacement in mA
    - Step in mA
    - Final wavelength displacement in mA

    E.g. lines = [['1', -500.0, 10.0, 1500.0], ['2', -750.0, 10.0, 1300.0]]

#### setPSF(lambda, transmission)
Define the spectral PSF to be convolved with the profiles. "lambda" is the displacement with respect to
the maximum in mA and "transmission" is the transmission of the PSF (it is normalized to unit area
in the code).
    
#### synthesize(model)
Carry out the synthesis and returns the Stokes parameters and the response functions to all physical variables at all depths.
    
    model (float array): an array of size [nDepth x 8], where the columns contain the depth stratification of:
    
    - log tau
    - Temperature [K]
    - Electron pressure [dyn cm^-2]
    - Microturbulent velocity [km/s]
    - Magnetic field strength [G]
    - Line-of-sight velocity [km/s]
    - Magnetic field inclination [deg]
    - Magnetic field azimuth [deg]
    
It returns:
    stokes: (float array) Stokes parameters, with the first index containing the wavelength displacement and the remaining
                                containing I, Q, U and V. Size (5,nLambda)
    rf: (float array) Response functions to T, Pe, vmic, B, v, theta, phi. Size (4,nLambda,nDepth)

#### Files
The following files are needed:

    - LINEAS: defines the available lines
    - THEVENIN: defines the abundances 
