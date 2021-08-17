
from multiR import *
import pickle
import os
import nibabel as nib
import numpy as np


def my_function(t):
    # print(t,I,s,eps)
    T1 = I.trajectories[s]
    T2 = I.trajectories[t]        
    connectEventList, disconnectEventList = findConnectDisconnectEvents(T1, T2, eps)
    return (connectEventList, disconnectEventList, t)

trkfolderO = '/home/shailja/Winter2021/Connectome/Data/old_trks/eps4_occ_mid_L/' #output folder to dump the disctionary
trkfolderI = '/home/shailja/Winter2021/Connectome/Data/old_trks/trk_occ_mid_L' #input track files
eps = 4 #granularity parameter
import pickle
# print(trkpath +".pickle")
trknamelist = os.listdir(trkfolderI)
for i in range(len(trknamelist)):
    # try:
    trkname = trknamelist[i]
    trkpathI = os.path.join(trkfolderI, trkname)
    trk = nib.streamlines.load(trkpathI)
    streamlines = trk.streamlines
    I = create_image(streamlines, eps )
    # dic_T = {}
    dic_T = {}

    for s in range(len(I.trajectories)):
        T1 = I.trajectories[s]
        dic_T[s] = {}    
        k1 = 0
        e1 = Event("appear", s)
        dic_T[s][k1] = [e1]
        k2 = len(T1.points) - 1
        e2 = Event("disappear", s)
        dic_T[s][k2] = [e2]
    # print(I)
    for s in range(len(I.trajectories)):
        myList = [i for i in range(s+1, len(I.trajectories))]
        inputs = tqdm(myList)
        pool = mp.Pool(processes = num_cores)
        processed_list = pool.map(my_function, inputs)
        pool.close()

        for i in range(len(processed_list)):
        	connectEventList = processed_list[i][0]
        	disconnectEventList = processed_list[i][1]
        	t = processed_list[i][2]
	        for c in connectEventList:
		        # print(c)
		        e = Event("connect",s, t, c[0], c[1])
		        if dic_T[s].get(c[0]):
		            dic_T[s][c[0]].append(e)
		        else:
		            dic_T[s][c[0]] = [e]
		        if dic_T[t].get(c[1]):                
		            dic_T[t][c[1]].append(e)
		        else:
		            dic_T[t][c[1]] =[e]
	        for c in disconnectEventList:
		        e = Event("disconnect",s, t, c[0], c[1])
		        if dic_T[s].get(c[0]):
		            dic_T[s][c[0]].append(e)
		        else:
		            dic_T[s][c[0]] = [e]
		        if dic_T[t].get(c[1]):                
		            dic_T[t][c[1]].append(e)
		        else:
		            dic_T[t][c[1]] =[e]
    # print(dic_T)

    with open(trkfolderO+trkname+".pickle", 'wb') as handle:
        pickle.dump(dic_T, handle, protocol=pickle.HIGHEST_PROTOCOL)
