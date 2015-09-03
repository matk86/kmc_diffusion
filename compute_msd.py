import os
import sys
import numpy as np
import time
import matplotlib.pyplot as plt
import math
from msd import compute

###############################################################################################################
# Flowchart to calcualte mean square displacement

# OLD METHOD

# 1. Say I have "N" trajectory with (t,x,y,z)
# 2. Then decide on time intervals at which we like to calcualte the displacement
# 3. Say, we break total time, into 1000 equal spaced time intervals
# 4. One has to be careful
#	A. This time interval may change for different KMC calculations, with changing strain and defect
#	B. Even, within same calculations, total time may not be exactly same
# 	C. Also, we may not have (x,y,z) values for exact of these time intervals
# 5. So, take the closed value of (x,y,z) for the desired time
# 6. Then calculate, square displacments for e.g sq.dis(x) = [(x(t)-(0)]**2 at each time interval, for all "N" trajectories
# 7. Calculate MSD(x) = sum(sq.dis(x),N) / N
# 8. Print, (t, MSD(x), MSD(y), MSD(z))

# NEW METHOD

# 1. sq.dis = [x(t+dt) - x(t)]**2
# 2. |--|-|------|----|--|--------|--|
#  t=0  2 3      9    13 15   	 24  26 sec
#  # 0  1 2      3    4  5        6  7
# take time interval as dt1 = 0-7
#			dt2 = 0-6, 1-7
#			dt3 = 0-5,1-6,2-7
# Note that you need to run inner loop within one time step dt, sq.dis for all "N" trajectories
# Also, dt will vary in all "N" different trjaectories, but make sure total steps are same and I think that dt will not vary very by large amount within same simulation should be close enough.

# 3. Need to chop of the trajectories to same steps
# 4. Calculate avg. value of dt
# 5. Then plot (avg.dt, MSD(x), MSD(y), MSD(z))	

# Write an additional script that calculate D(x), D(y) and D(z) from relation: MSD(i) = 2*D(i)*t and in desired units

# Check some of these scripts here, as they may be useful:https://pythonhosted.org/SLOTH/Module.html#sloth.mean_square_analyser.lq_diffusion_fit_constrained
#############################################################################################################


def compute_msd(d):
        time = d[:,0]
	trajectory = d[:, 1:]
	avg_dt = []
	avg_dx2 = []
	avg_dy2 = []
	avg_dz2 = []

	n = len(time)
	for i in range(1, n):
                dt = time[i:] - time[:-i]
                dx2 = (trajectory[i:,0] - trajectory[:-i,0])**2
                dy2 = (trajectory[i:,1] - trajectory[:-i,1])**2
                dz2 = (trajectory[i:,2] - trajectory[:-i, 2])**2

                avg_dt.append(dt.mean())
                avg_dx2.append(dx2.mean())
                avg_dy2.append(dy2.mean())
                avg_dz2.append(dz2.mean())

	return  np.array(avg_dt), np.array(avg_dx2), np.array(avg_dy2), np.array(avg_dz2)
	
# Open all trajectory "N" files from a directory and read them into an array
def post_process(N=1000, chop=1000):
        flog = open('msd.log','w')
        DATA = []
        dirname = '.'
        file_list = [dirname+os.sep+str(i) for i in range(N)]
        length = []

        for file in file_list:
                flog.write('in directory, '+os.getcwd()+' processing file(trajectory) :'+file+'\n')
                # Array size (N,t,x,y,z)
                data = np.loadtxt(file, skiprows=1)
                length.append(data.shape[0])
                DATA.append(data)	

        l_min = min(length)
        final_len = l_min-1-chop 
        tfinal = np.zeros(final_len)
        x2final = np.zeros(final_len)
        y2final = np.zeros(final_len)
        z2final = np.zeros(final_len)

        ttime = 0.0

        for i, d in enumerate(DATA):
                flog.write('computing msd for trajectory : '+str(i)+'\n')
                n = len(d[:,0])
                dt = np.zeros(n)
                dx2 = np.zeros(n)
                dy2 = np.zeros(n)
                dz2 = np.zeros(n)
                t = np.asfortranarray(d[:,0])
                x = np.asfortranarray(d[:,1])
                y = np.asfortranarray(d[:,2])
                z = np.asfortranarray(d[:,3])    

                start = time.time()
                dt,dx2,dy2,dz2 = compute(t,x,y,z, dt, dx2, dy2, dz2, n)
                #t,x2,y2,z2 =compute_msd(d)
                end = time.time()
                flog.write('computed the msd in time = '+str(end-start)+'\n')
                ttime = ttime + (end-start)
                tfinal = tfinal + dt[:final_len]
                x2final = x2final + dx2[:final_len]
                y2final = y2final + dy2[:final_len]
                z2final = z2final + dz2[:final_len]

        #average over the trajectories
        tfinal = tfinal /N 
        x2final = x2final /N
        y2final = y2final /N
        z2final = z2final /N
        d2final = x2final + y2final + z2final

        coeffx = np.polyfit(tfinal, x2final, 1)
        coeffy = np.polyfit(tfinal, y2final, 1)
        coeffz = np.polyfit(tfinal, z2final, 1)
        coeffd = np.polyfit(tfinal, d2final, 1)

        #plt.plot(tfinal, x2final, 'ro', label='x')
        #plt.plot(tfinal, y2final, 'g*', label='y')
        #plt.plot(tfinal, z2final, 'b+', label='z')
        #plt.legend()
        #plt.savefig('msd.png')

        Dx = coeffx[0]/(2.0*(10**20))
        Dy = coeffy[0]/(2.0*(10**20))
        Dz = coeffz[0]/(2.0*(10**20))
        DD = coeffd[0]/(6.0*(10**20))#math.sqrt((Dx**2) + (Dy**2) + (Dz**2))

        # Open a file to write down MSD
        f2 = open('MSD.dat', 'w')
        f2.write('# time '+str(ttime)+'\n')
        f2.write('# slope Dx Dy Dz\n')
        f2.write(str(coeffx[0])+' '+str(coeffy[0])+' '+str(coeffz[0])+'\n')
        f2.write('# Dx Dy Dz DD\n')
        f2.write(str(Dx)+' '+str(Dy)+' '+str(Dz)+' '+str(DD)+'\n')
        np.savetxt(f2, np.c_[tfinal,x2final,y2final,z2final],fmt='%12.5f')
        f2.close()
        flog.close()
        return
