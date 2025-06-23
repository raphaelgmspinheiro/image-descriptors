#! /usr/bin/python

import sys
import pickle as cPickle
from scipy.stats.kde import gaussian_kde
from scipy.integrate import quad,simps
import math
import scipy
import scipy.stats
import descriptors as descritores
import time
import multiprocessing
from multiprocessing import Process, Queue
import numpy as np
import pylab


def desc_entropy(fn,s):
 k = descritores.curvatura(fn,s[::-1])
 #hist = scipy.vstack([scipy.stats.histogram(a,numbins = 2500,defaultlimits = (-250.,250.)) for a in k.curvs])
 h = []
 for c,contour in zip(k.curvs,k.contours):
#  print c.shape
#  print c.min(),c.max()
  #caux = scipy.tanh(c)
  caux = c
  my_pdf = gaussian_kde(caux)
#  my_pdf = gaussian_kde(caux,'silverman')  
#O termo "+scipy.log(contour.perimeter())" eh utilizado a seguir afim de que o descritor seja invariavel a escala
#h(aX)=h(X)+log(a)
  #h = quad(lambda x: -pdf(x)*pylab.log(pdf(x)+1e-12),c.mean()-5*c.std(),c.mean()+5*c.std())[0]
  h.append(quad(lambda x: -my_pdf(x)*pylab.log(my_pdf(x)+1e-12),c.mean()-5*c.std(),c.mean()+5*c.std())[0])#+scipy.log(contour.perimeter()))
  #t = scipy.linspace(caux.min(),caux.max(),350)
#  h.append(simps(-my_pdf(t)*scipy.log(my_pdf(t)+1e-12),t) + scipy.log(contour.perimeter()))
 #H(my_pdf(x)/my_pdf(x).max())) 
 return scipy.array(h)
 
def dict_desc_entropy(diretorio,cl,index_list,sigma,q):
 db = {}
 for im_file in np.array(list(cl.keys()))[index_list]:
  db[im_file]  = desc_entropy(diretorio+im_file,sigma)[0:-1]
  db[im_file] = scipy.hstack((cl[im_file],db[im_file]))
  #print im_file,db[im_file]
 q.put(db)


def entropia_diferencial_curvatura(descriptor_params,database_dir,database_classes):
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
        process_list[i] = Process(target=dict_desc_entropy, args=(diretorio,cl,range(i*passo,(i+1)*passo),sigma,queue_list[i]))
        process_list[i].start()
    
    i=i+1
    queue_list[i]=Queue()
    process_list[num_cores-1] = Process(target=dict_desc_entropy, args=(diretorio,cl,range(i*passo,len_cl),sigma,queue_list[i]))
    process_list[num_cores-1].start()    

    for j in range(num_cores):
        db.update(queue_list[j].get())
    
    #espera ate todos os processos terminarem
    for k in range(num_cores):
        process_list[k].join()

    return db
