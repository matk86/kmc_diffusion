- KMC_run.py

  	Python wrapper to launch kMC jobs concurrently
	
- compute_msd.py

	Compute mean square displacement (msd) vs. time and diffusivities
	from the kMC outputs.
- msd.f90

	F90 code used to perform the numerically intensive mean square displacement computation.
	Compiled using f2py and used in compute_msd.py
