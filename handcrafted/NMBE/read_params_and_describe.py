# -*- coding: utf-8 -*-
"""
Created on Sun Oct 09 02:50:45 2016
@author: ALLAN
"""
import os
import pickle
import numpy as np
from functools import partial
from nmbe_multi import nmbe


def process_data(file_name):
    data = open(file_name).readlines()
    data = [line.strip('') for line in data]
    data = [line.replace(']', '') for line in data]
    data = [line.replace('[', '') for line in data]

    return np.loadtxt(data)


if __name__ == '__main__':

    im_database_dir = 'C:/Users/rapha/Desktop/TextureDescriptors/MED115/MED115_bin_all/'
    params_dir = 'C:/Users/rapha/Desktop/TextureDescriptors/MED115/to_describe/'
    result_dir = 'C:/Users/rapha/Desktop/TextureDescriptors/MED115/to_describe/describe_nmbe/'

    #CUIDADO COM O OS.LISTDIR
    file_names_list = os.listdir(params_dir)
    file_names_list = file_names_list[1::]

    descriptor_function = partial(nmbe, database_dir=im_database_dir,
                                  database_classes=np.load(im_database_dir + 'classes.txt', allow_pickle=True))

    i = 0
    n_files = len(file_names_list)

    for file_name in file_names_list:
        #print(params_dir)
       # print(file_name)
        data = process_data(params_dir + file_name)
        dic_db = descriptor_function(descriptor_params=data[-1, 2:])

        fd = open(result_dir + file_name[0:file_name.rindex('.')] + '.db', 'wb')
        pickle.dump(dic_db, fd)
        fd.close()

        i = i + 1
        print('%.2f' % (100 * i / n_files), '%')