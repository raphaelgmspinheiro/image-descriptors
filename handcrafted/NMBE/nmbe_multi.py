#! /usr/bin/python

import sys
from scipy.stats.kde import gaussian_kde
from scipy.integrate import quad,simps
import math
import scipy
import scipy.stats
import descriptors
import time
import multiprocessing
from multiprocessing import Process, Queue
import numpy as np

def dict_desc_nmbe(diretorio,cl,index_list,sigma,q):
    db = {}
    
    for im_file in np.array(list(cl.keys()))[index_list]:
        
        a=[]
        nmbe=descriptors.bendenergy(diretorio+im_file,sigma)()
        for i in nmbe:
            a.append(i)
        #db[im_file]  = np.log(a)
        db[im_file] = np.log(np.maximum(a, 1e-8))
        db[im_file] = scipy.hstack((cl[im_file],db[im_file]))
        #print im_file,db[im_file]
    q.put(db)
 

def nmbe(descriptor_params,database_dir,database_classes):
    diretorio = database_dir

    cl=database_classes

    
    sigma=descriptor_params
    
    #tt = time.time()
    db = {}
    #print "feature extraction"
    
    num_cores = multiprocessing.cpu_count()
    process_list=[None]*num_cores
    queue_list=[None]*num_cores

    len_cl=len(cl)
    passo=len_cl//num_cores
    
    for i in range(num_cores-1):
        queue_list[i]=Queue()
        process_list[i] = Process(target=dict_desc_nmbe, args=(diretorio,cl,range(i*passo,(i+1)*passo),sigma,queue_list[i]))
        process_list[i].start()
    
    i=i+1
    queue_list[i]=Queue()
    process_list[num_cores-1] = Process(target=dict_desc_nmbe, args=(diretorio,cl,range(i*passo,len_cl),sigma,queue_list[i]))
    process_list[num_cores-1].start()    

    for j in range(num_cores):
        db.update(queue_list[j].get())
    
    #wait for all process
    for k in range(num_cores):
        process_list[k].join()

    return db