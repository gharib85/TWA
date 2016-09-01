# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 13:34:22 2016

@author: Jonathan Wurtz
"""

# Parses output files which are copied here...
import os
from numpy import *

def old_parse(filename):
    #filename = 'small_mottIC.o57511-'
    os.chdir('C:\Users\Jonathan Wurtz\Documents\Research\Scripts\SU3_dynamics\Outputs_0826')
    filed = os.listdir(os.getcwd())
    
    f = open(filename+'0')
    
    
    
    header = []
    for i in range(8):
        header.append(f.readline())
        
    ff = f.readline()
    datstring = ''
    while ff:
        if 'D' not in ff and '[' not in ff:
            datstring +=ff
        ff = f.readline()
        
    dat = genfromtxt(StringIO(datstring))
    f.close()
    n_tsteps = 1.0*dat.shape[0]/int(header[6])
    
    if round(n_tsteps)!=n_tsteps:
        raise 'Bad!'
        
    dat_out = dat.reshape(int(header[6]),n_tsteps,3).sum(0)/int(header[6])
    kk = 1
    
    
    for k in filed:
        if filename in k:
            print 'ping'
            f = open(k)
            for i in range(8):
                f.readline()
            
            ff = f.readline()
            datstring = ''
            while ff:
                if 'D' not in ff and '[' not in ff:
                    datstring +=ff+str('\n')
                ff = f.readline()
            dat_out += genfromtxt(StringIO(datstring)).reshape(int(header[6]),n_tsteps,3).sum(0)/int(header[6])
            kk+=1
    dat_out = dat_out/kk
    figure()
    plot(dat_out[:,0],dat_out[:,2])
    title('Bose Hubbard Model, IC: '+header[5]+'(J,U)=('+header[1][0:-1]+', '+header[2][0:-1]+')\n Number of Trials:'+repr(kk*int(header[6]))+'\n tstep: '+header[7][0:-1]+'\nData:'+filename)
    xlabel('Scaled Time tU')
    ylabel('Order Parameter')

def new_parse(filename):
    # Array number replaced with *
    #filename = 'FILE{57528[*].buphyg.bu.edu}.dat'
    os.chdir('C:\Users\Jonathan Wurtz\Documents\Research\Scripts\SU3_dynamics\Outputs_0826')
    filed = os.listdir(os.getcwd())
    touse = []
    # Find number of files of the same type...
    for i in range(128): # Ug, lazy solution... what if you ahve more then 128 jobs?
        if filename.replace('*',str(i)) in filed and filename.replace('*',str(i)) not in touse:
            touse.append(filename.replace('*',str(i)))
        
        
    f = open(touse[0])
    nlines = int(f.readline().split(':')[1])
    config_data = {}
    for i in range(nlines):
        line = f.readline()
        linesplit = line.split(':')
        config_data[linesplit[0].strip()]=linesplit[1].strip()
    
    # Now we know how many cycles there are!
    len_t = int(double(config_data['T'])/double(config_data['tobs']))+1
    dat_out = zeros([len_t,len(touse)*int(config_data['ncycles'])])
    T_out = zeros(len_t)
    ind = 0
    
    dat_temp0 = array(genfromtxt(f))
    nc = 2*int(config_data['ncycles'])
    dat_temp = dat_temp0.transpose().reshape(nc,len_t) #ugh.
    ind = 0
    for ll in range(dat_temp.shape[0]/2):
        dat_out[:,ll] = dat_temp[ll+2,:].transpose()
    
    T_out = dat_temp[0,:]
    f.close()
    for touse_ in touse[1::]:
        ind+=1
        f = open(touse_)
        for i in range(nlines+1):
            f.readline()
        dat_temp0 = array(genfromtxt(f))
        dat_temp = dat_temp0.transpose().reshape(nc,len_t) #ugh.
        
        for ll in range(dat_temp.shape[0]/2):
            dat_out[:,ll+nc/2*ind] = dat_temp[ll+2,:].transpose()
        
        f.close()
    
    plot(T_out,average(dat_out,axis=1),'b',linewidth=2)
    plot(T_out,average(dat_out,axis=1)+std(dat_out,axis=1)/sqrt(dat_out.shape[1]),'r--',linewidth=1)
    plot(T_out,average(dat_out,axis=1)-std(dat_out,axis=1)/sqrt(dat_out.shape[1]),'r--',linewidth=1)
    xlabel('Scale Time')
    ylabel('Order Parameter')
    return T_out,dat_out,config_data
'''

#return dat_temp    


    
    
    
'''