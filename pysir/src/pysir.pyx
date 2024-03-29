# cython: language_level=3
from numpy cimport ndarray as ar
from numpy import empty, ascontiguousarray
import numpy as np

cdef extern:
	void c_init(int *nLambda)
	void c_setpsf(int *nPSF, float *xPSF, float *yPSF)
	void c_synthrf(int *nDepth, int *nLambda, int *nLines, float *macroturbulence, float *filling, float *stray, float *model, float *departure, float *stokes, float *rt, float *rp, float *rh,
		float *rv, float *rf, float *rg, float *rm, float *rmac)
	void c_synth(int *nDepth, int *nLambda, int *nLines, float *macroturbulence, float *filling, float *stray, float *model, float *departure, float *stokes)

cdef int nLambdaGlobal = 1

def init():
	cdef:
		int nLambda

	global nLambdaGlobal
	
	c_init(&nLambda)

	nLambdaGlobal = nLambda

	return nLambda

def setPSF(ar[float, ndim=1] xPSF, ar[float, ndim=1] yPSF):
	cdef:
		int nLambdaPSF = xPSF.shape[0]

	c_setpsf(&nLambdaPSF, &xPSF[0], &yPSF[0])

	return

def synth(ar[float, ndim=2] modelIn, ar[float, ndim=3] departureIn, float macroturbulence, float filling, float stray):

	cdef:
		int nLambda = nLambdaGlobal
		int nDepth = modelIn.shape[0]
		int nLines = departureIn.shape[1]
		ar[float, ndim=2, mode="c"] model
		ar[float, ndim=3, mode="c"] departure
		ar[float, ndim=2] stokes = empty((5,nLambda), order='F', dtype=np.float32)
		
	# Make sure that the 2D array is C_CONTIGUOUS
	model = ascontiguousarray(modelIn)
	departure = ascontiguousarray(departureIn)

	c_synth(&nDepth, &nLambda, &nLines, &macroturbulence, &filling, &stray, &model[0,0], &departure[0,0,0], <float*> stokes.data)
	
	return stokes

def synthRF(ar[float, ndim=2] modelIn, ar[float, ndim=3] departureIn, float macroturbulence, float filling, float stray):

	cdef:
		int nLambda = nLambdaGlobal
		int nDepth = modelIn.shape[0]
		int nLines = departureIn.shape[1]
		ar[float, ndim=2, mode="c"] model
		ar[float, ndim=3, mode="c"] departure
		ar[float, ndim=2] stokes = empty((5,nLambda), order='F', dtype=np.float32)
		ar[float, ndim=3] rt = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=3] rp = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=3] rh = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=3] rv = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=3] rf = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=3] rg = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=3] rm = empty((4,nLambda,nDepth), order='F', dtype=np.float32)
		ar[float, ndim=2] rmac = empty((4,nLambda), order='F', dtype=np.float32)
		
	# Make sure that the 2D array is C_CONTIGUOUS
	model = ascontiguousarray(modelIn)
	departure = ascontiguousarray(departureIn)

	c_synthrf(&nDepth, &nLambda, &nLines, &macroturbulence, &filling, &stray, &model[0,0], &departure[0,0,0], <float*> stokes.data, <float*> rt.data, <float*> rp.data, 
		<float*> rh.data, <float*> rv.data, <float*> rf.data, <float*> rg.data, <float*> rm.data, <float*> rmac.data)
	
	return stokes, [rt, rp, rh, rv, rf, rg, rm, rmac]