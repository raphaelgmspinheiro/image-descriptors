# -*- coding: utf-8 -*-
"""
Created on Wed May 04 09:35:07 2016

@author: ALLAN
"""
import numpy as np
import time


def sa(fitness,search_range,N_iterations,T0,alpha,L,step):
    # Parametros
    
    #N_iterations -> Number of iterations
    #N_candidates -> Number of candidate solutions
    #search_range -> Search space
    
    # Number of parameters to be optimized
    N_parameters = search_range.shape[0]
    #s -> Current solution
    
    T=T0
    
    # Generate initial solution
    s=np.random.random(N_parameters)
    for i in range(N_parameters):
        inf=search_range[i,0]
        sup=search_range[i,1]
        s[i]=((sup-inf)*s[i])+inf
    
        
    fit_s=fitness(s)
    
    fit_s_vector=np.zeros(N_iterations+1)
    fit_s_vector[0]=fit_s
    
    for i in range(N_iterations):
        for k in range(L):
            s_trial=s+step*s*(2*np.random.random(N_parameters)-1)
    
            for j in range(N_parameters):
                
                inf=search_range[j,0]
                sup=search_range[j,1]
                    
                if s_trial[j]>sup:
                    s_trial[j]=sup
                    
                elif s_trial[j]<inf:
                    s_trial[j]=inf
                
            fit_s_trial=fitness(s_trial)
            delta=fit_s_trial-fit_s
                
            if delta<=0 or np.exp(-delta/T)>np.random.random():
                s=s_trial
        
        T=alpha*T
        
        fit_s=fitness(s)
        fit_s_vector[i+1]=fit_s

        print (i, -fit_s , s)

    return [s,fit_s_vector]