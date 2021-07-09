import os
import nibabel as nib
import numpy as np
import networkx as nx
from reeb_grapher import *
import pickle

trkfolder = '/mnt/c/Users/shail/Documents/Connectome/Connectome/Data/trk/eps3'
trkfolderI = '/mnt/c/Users/shail/Documents/Connectome/Connectome/Data/trk/raw_data'
eps = 3

trknamelist = os.listdir(trkfolder)
for trk_i in range(len(trknamelist)):    
    trkname = trknamelist[trk_i]
    trkpathI = os.path.join(trkfolderI, trkname[:len(trknamelist[trk_i])-7])
    trk = nib.streamlines.load(trkpathI)
    streamlines = trk.streamlines
    I = create_image(streamlines, eps)

    trkpath = os.path.join(trkfolder, trkname)

    with open(trkpath, 'rb') as handle:
        dic_T = pickle.load(handle)

    #construct Reeb graph R
    R = nx.Graph()
    check_traj = np.zeros((len(I.trajectories), 2000), dtype=bool) #Flag considered points of the trajectories; we are assuming if each trajetcory has a maximum of 2000 points
    tree_node_map = {} #for final merge
    node_coordinate_map = {} #for location of nodes
    nc = 0 #node count
    for s in range(len(I.trajectories)): #start with trajectories in I one by one
        # print("Processing trajectory", s)
        M = {}
        prev_connected_comp = []
        T1 = I.trajectories[s]
        trajectory_to_node_map_pres = {}
        trajectory_to_node_map_prev = {}
        if not (check_traj[s][0]): #check first point of the trajectory (if first is already considered then all following points are already considered)
            G = nx.Graph() # This graph will be modified dynamically
            traj_list = [s] # all trajectories to be taken into acount in this batch
            ind_list = [0] #corresponding indices of above
            while (len(traj_list)>0): #go on till the trajectories to be considered have not exhausted
                del_ind_tra = []
                disconnected_events = []
                disappear_events = []
                eventFlag = False
                i = 0
                delete_nodes = []
                while (i < len(traj_list)):
                    if not (check_traj[traj_list[i]][ind_list[i]]):                   
                        check_traj[traj_list[i]][ind_list[i]] = True
                        if dic_T[traj_list[i]].get(ind_list[i]):
                            events = dic_T[traj_list[i]][ind_list[i]]                        
                            for e in events:
                                if not e.considered:                            
                                    eventFlag = True
                                    if e.event == "appear":
    #                                     print("Appear ", e.trajectory1)
                                        G.add_node(traj_list[i])                                     
                                        e.considered = True
                                        if e.trajectory1 not in traj_list:
                                            print("WARNING!!!!")
                                        
                                    elif e.event == "connect":
    #                                     print("Connected event between", e.trajectory1, e.trajectory2)
                                        G.add_node(e.trajectory2)
                                        G.add_node(e.trajectory1)
                                        G.add_edge( e.trajectory1, e.trajectory2)
                                        
                                        if e.trajectory2 not in traj_list:
                                            traj_list.append(e.trajectory2)
                                            ind_list.append(e.t2)
                                            connect_j = []
                                            temp_dic = {}
                                            for j in range(e.t2): # to handle events before non zero index
                                                if  dic_T[e.trajectory2].get(j):
                                                    eventj = dic_T[e.trajectory2][j]   #event at index j                                      
                                                    for ej in eventj:
                                                        if(ej.event == "connect"):
                                                            if (ej.trajectory2 != e.trajectory2):
                                                                connect_j.append(ej.trajectory2)
                                                                temp_dic[ej.trajectory2] = [j, ej.t2]
                                                            else:
                                                                connect_j.append(ej.trajectory1)
                                                                temp_dic[ej.trajectory1] = [j, ej.t1]
                                                                
                                                        elif(ej.event == "disconnect"):
                                                            if ej.trajectory2 in connect_j:
                                                                connect_j.remove(ej.trajectory2)
                                                            elif ej.trajectory1 in connect_j:
                                                                connect_j.remove(ej.trajectory1)
                                                        
                                            for c in connect_j:
                                                G.add_node(c)
                                                G.add_edge(e.trajectory2, c) 
                                                if c not in traj_list:
                                                    traj_list.append(c)
                #                                     e.t2 - j = x- ej.t2 from assumption
                                                    ind_list.append(temp_dic[c][1] - temp_dic[c][0] + e.t2)
    #                                     else:
    #                                         x = traj_list.index(e.trajectory2)
    #                                         y = ind_list[x]
    #                                         if (e.t2 < y):
    #                                             ind_list[x] = e.t2
                                                
                                        
                                        if e.trajectory1 not in traj_list:
                                            traj_list.append(e.trajectory1)
                                            ind_list.append(e.t1)
                                            connect_j = []
                                            temp_dic = {}
            #                                 print("e.t2", e.t2)
                                            for j in range(e.t1): # to handle events before non zero index

                                                if  dic_T[e.trajectory1].get(j):
                                                    eventj = dic_T[e.trajectory1][j]   #event at index j                                      
                                                    for ej in eventj:
                                                        if(ej.event == "connect"):
                                                            if(ej.trajectory1 != e.trajectory1):
                                                                connect_j.append(ej.trajectory1)
                                                                temp_dic[ej.trajectory1] = [j, ej.t1]
                                                            else:
                                                                connect_j.append(ej.trajectory2)
                                                                temp_dic[ej.trajectory2] = [j, ej.t2]
                                                                
                                                        elif(ej.event == "disconnect"):
                                                            if ej.trajectory1 in connect_j:
                                                                connect_j.remove(ej.trajectory1)
                                                            elif ej.trajectory2 in connect_j:
                                                                connect_j.remove(ej.trajectory2)

                                            for c in connect_j:
                                                G.add_node(c)
                                                G.add_edge(e.trajectory1, c)
                                                if c not in traj_list:
                                                    traj_list.append(c)
                #                                     e.t2 - j = x- ej.t2 from assumption
                                                    ind_list.append(temp_dic[c][1] - temp_dic[c][0] + e.t1)
    #                                             else:
    #                                                 x = traj_list.index(c)
    #                                                 y = ind_list[x]
    #                                                 if (temp_dic[c][1] - temp_dic[c][0] + e.t1 < y):
    #                                                     ind_list[x] = y
                                                    
    #                                     else:
    #                                         x = traj_list.index(e.trajectory1)
    #                                         y = ind_list[x]
    #                                         if (e.t1 < y):
    #                                             ind_list[x] = y
                                        e.considered = True
                                    elif (e.event == "disconnect"):
    #                                     print("Disconnected event between", e.trajectory1, e.trajectory2)
                                        if (G.has_node (e.trajectory2) and G.has_node (e.trajectory1)): 
                                            disconnected_events.append(e)
                                            if (G.has_edge(e.trajectory1, e.trajectory2)):            
                                                G.remove_edge(e.trajectory1, e.trajectory2)
                                                e.considered = True
                                            #if trajectory is not present what to delete
    #                                         if e.trajectory2 not in traj_list:
    #                                             traj_list.append(e.trajectory2)
    #                                             ind_list.append(e.t2)
    #                                         elif e.trajectory1 not in traj_list:
    #                                             traj_list.append(e.trajectory1)
    #                                             ind_list.append(e.t1)
                                            
                                        else:
                                            check_traj[traj_list[i]][ind_list[i]] = False
                                    
                                    elif (e.event == "disappear"):
                                        disappear_events.append(e)
                                        delete_nodes.append(traj_list[i])
                                        del_ind_tra.append(i)
                                        e.considered = True
                                
                                
                                    
                    else:                    
                        delete_nodes.append(traj_list[i])
                        del_ind_tra.append(i)
    #                     print("REACHED HERE FINALLY", traj_list[i], M, ind_list[i])
                        if (trajectory_to_node_map_prev.get(traj_list[i])):
                            R.add_edge(M[trajectory_to_node_map_prev[traj_list[i]]], tree_node_map[traj_list[i]] )
    #                     if G.has_node(traj_list[i]):
    #                         G.remove_node(traj_list[i])
    #                     traj_list.remove(traj_list[i])
    #                     ind_list.remove(ind_list[i])
                        
    #                 print("Trajectory list", traj_list)
    #                 print("Index list", ind_list)    
                    i += 1
                if (eventFlag):
    #                 print(M)
                    
    #                 print("connected component")
    #                 for c in nx.connected_components(G):
    #                     print(c)
                    
                    if (len(prev_connected_comp) == 0): # this will be executed only once
                        
                        prev_connected_comp = [c for c in nx.connected_components(G)]
                        for prev_cc in prev_connected_comp:
                            R.add_node(nc)
                            M[frozenset(prev_cc)] = nc
                            for ci in prev_cc:
                                trajectory_to_node_map_prev[ci] = frozenset(prev_cc)
                                if not tree_node_map.get(ci):
                                    tree_node_map[ci] = nc
                            #node_coordinate_map[nc] = I.trajectories[traj_list[traj_list.index(list(prev_cc)[0])]].points[ind_list[traj_list.index(list(prev_cc)[0])]]
                            nc += 1

                    else:
                        pres_connected_component = [c for c in nx.connected_components(G)]
                        for pres_cc in pres_connected_component:
                            for ci in pres_cc:
                                trajectory_to_node_map_pres[ci] = frozenset(pres_cc)
                                for c_individual in pres_cc:
                                    if not tree_node_map.get(c_individual):
                                        tree_node_map[c_individual] = nc
                            
                        copied_nodes = [] #this will store all split events
                        if len(disconnected_events) != 0:
                            
                            for de in disconnected_events:
                                C1 = None
                                C2 = None
                                if trajectory_to_node_map_prev.get(de.trajectory1):                                
                                    C1 = trajectory_to_node_map_prev[de.trajectory1]
                                else:
                                    check_traj[de.trajectory1][de.t1] = False
                                if trajectory_to_node_map_prev.get(de.trajectory2):
                                    C2 = trajectory_to_node_map_prev[de.trajectory2]
                                else:
                                    check_traj[de.trajectory2][de.t2] = False                            
                                if (C1 == None and C2 == None):
                                    continue

                                elif (C1 != C2):
                                    continue
                                    
                                elif C1 not in copied_nodes and (trajectory_to_node_map_pres[de.trajectory1] != trajectory_to_node_map_prev[de.trajectory1]):
                                    
                                    R.add_node(nc)                            
                                    R.add_edge(M[C1],nc)
                                    copied_nodes.append(C1)
                                    M[frozenset(C1)] = nc
    #                                 try:
    #                                     node_coordinate_map[nc] = I.trajectories[traj_list[traj_list.index(de.trajectory1)]].points[ind_list[traj_list.index(de.trajectory1)]-1]
    #                                 except:
    #                                     print("node", nc, C1)
                                    nc += 1
                                    
                        
                        for cc in pres_connected_component:
                            if cc in prev_connected_comp:#do nothing: still epsilon connected
                                continue

                            else:
                                check = False
                                check_cc = False
                                for cn in copied_nodes:
                                    if cc.issubset(cn):
                                        M[frozenset(cc)] = M[frozenset(cn)]
                                        check_cc = True
                                if not check_cc:
                                    
                                        
                                    for prev_cc in prev_connected_comp:
                                        #add edge if nodes are neighbor
                                        if prev_cc.intersection(cc):
                                            check = True
                                            R.add_node(nc)
                                            M[frozenset(cc)] = nc
    #                                         try:                                      
    #                                         node_coordinate_map[nc] = I.trajectories[list(cc)[0]].points[ind_list[traj_list.index(list(cc)[0])]]
    #     #                                     print("check here please",prev_connected_comp, cc)
    #                                         except:
    #                                             print("Line 212", nc, cc)
                                            R.add_edge(M[frozenset(prev_cc)], M[frozenset(cc)])
                                            for c_individual in cc:
                                                if not tree_node_map.get(c_individual):
                                                    tree_node_map[c_individual] = nc


        #                                     print("added edge between: ", prev_cc, cc, "node ids are", M[frozenset(prev_cc)], M[frozenset(cc)])

                                        if not check:
                                            R.add_node(nc)
                                            M[frozenset(cc)] = nc
    #                                         try:
    #                                             node_coordinate_map[nc] = I.trajectories[traj_list[traj_list.index(list(cc)[0])]].points[ind_list[traj_list.index(list(cc)[0])]]
    #                                         except:
    #                                             print(nc, cc)
                                            for c_individual in cc:
                                                if not tree_node_map.get(c_individual):
                                                    tree_node_map[c_individual] = nc

                                        nc += 1
                        if (len(disappear_events) != 0):
                            for da in disappear_events:
                                C1 = None                            
                                if trajectory_to_node_map_prev.get(da.trajectory1):                                
                                    C1 = trajectory_to_node_map_prev[da.trajectory1]
                                    check = False    
                                    if len(C1) == 1:
                                        for x in range(len(I.trajectories[list(C1)[0]].points)):
                                            if dic_T[list(C1)[0]].get(x) and "connect" in [y.event for y in dic_T[list(C1)[0]][x]]:
                                                check = True
                                                continue
                                        if check and C1 in prev_connected_comp:
                                                pc = M[frozenset(C1)]                                    
    #                                             node_coordinate_map[pc] = I.trajectories[traj_list[traj_list.index(list(C1)[0])]].points[-1]
                                        
                                        else:
                                            
                                            R.add_node(nc)                            
                                            R.add_edge(M[C1],nc)                                    
                                            M[frozenset(C1)] = nc                                        
    #                                         node_coordinate_map[nc] = I.trajectories[da.trajectory1].points[-1]                                        
                                            nc += 1
                                    
                                
                            
                
                        prev_connected_comp = []
                        for cx in pres_connected_component :
                            prev_connected_comp.append(cx)
                                            
                        trajectory_to_node_map_prev = trajectory_to_node_map_pres
                        trajectory_to_node_map_pres = {}
                    
    #                 print("Shailja", R.nodes, R.edges)
                    for node in delete_nodes:
                        if G.has_node(node):
                            G.remove_node(node)
                    
                        

                ind_list = [x+1 for x in ind_list]
                
                for j in range(len(traj_list)):
                    if (ind_list[j] >= len(I.trajectories[traj_list[j]].points)):
                        del_ind_tra.append(j)                    
                
                traj_list = [i for j, i in enumerate(traj_list) if j not in del_ind_tra]
                ind_list = [i for j, i in enumerate(ind_list) if j not in del_ind_tra]
    print(trkname, len(streamlines), len(R.nodes()), len(R.edges()))      
