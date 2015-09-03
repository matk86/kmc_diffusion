import numpy as np
import os
import sys
import subprocess as sp
import shutil
import glob

from multiprocessing import Pool

from compute_msd import post_process
from itertools import *

def main(args):
        (i, N, chop) = args
        inp_file_list = glob.glob('UVAC.*')
        parent_dir = '.'
        command = ['okmc', 'UVAC']
        dirname = str(i)
        print 'changing to directory ...', dirname
        for in_file in inp_file_list:
                shutil.copy(in_file, dirname+os.sep+in_file)
        os.chdir(dirname)
        print 'running in .. ', dirname
        for it in range(N):
                #with open('job.out', 'w') as f:
                #        p = sp.Popen(command, stdout=f, stderr=f)
                # Since we are using the external binary, we need to run the command using subprocess below
		p = sp.Popen(command)
                p.wait()
                shutil.copy('OUTPUT', str(it))
        #process all trajectories
        post_process(N=N, chop=chop)
        #clean up
        for it in range(N):
                os.remove(str(it))
        return

if __name__=='__main__':
        N = 1000 #number of trajectories
        chop = 2000
	#number of process should be equal to count
        #n_processes = 30
	count = 15
	
        p = Pool(count)
        p.map(main, [ (i, N,chop) for i in range(0,15) ] )
